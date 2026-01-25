# dearpygui_ips_patcher_fixed2_nosame.py
"""
DearPyGui IPS patcher — Up/Down/Info callbacks using DPG user_data
Replaces deprecated add_same_line() with horizontal groups.
Defaults to ./patches if present.
"""
import os
import hashlib
import zlib
from collections import defaultdict
import traceback

import dearpygui.dearpygui as dpg

# -------------------------------
# CONFIG: Known clean FireRed ROM hashes
# -------------------------------
KNOWN_ROMS = {
    "Pokemon FireRed USA v1.0": {
        "crc32": "DD88761C",
        "sha1": "41CB23D8DCCC8EBD7C649CD8FBB58EEACE6E2FDC"
    }
}

# -------------------------------
# App state (default patches dir = ./patches if present)
# -------------------------------
DEFAULT_PATCHES_DIR = os.path.join(os.getcwd(), "patches")
APP_STATE = {
    "base_rom": None,
    "patches_dir": DEFAULT_PATCHES_DIR if os.path.isdir(DEFAULT_PATCHES_DIR) else None,
    "patches_order": [],  # list of filenames in current order
}

# -------------------------------
# Helpers
# -------------------------------
def sanitize_tag(s: str) -> str:
    # produce a safe tag for dearpygui from filename
    return "tag::" + "".join(c if c.isalnum() or c in "-_." else "_" for c in s)

def compute_hashes(path):
    crc = 0
    sha1 = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            crc = zlib.crc32(chunk, crc)
            sha1.update(chunk)
    return f"{crc & 0xFFFFFFFF:08X}", sha1.hexdigest().upper()

# -------------------------------
# IPS parsing / apply (unchanged logic)
# -------------------------------
def parse_ips_ranges(ips_path):
    ranges = []
    with open(ips_path, "rb") as f:
        header = f.read(5)
        if header != b"PATCH":
            raise ValueError(f"{ips_path} is not a valid IPS (missing PATCH header)")
        while True:
            offset_bytes = f.read(3)
            if not offset_bytes:
                raise ValueError(f"Unexpected EOF in IPS: {ips_path}")
            if offset_bytes == b"EOF":
                break
            offset = int.from_bytes(offset_bytes, "big")
            size_bytes = f.read(2)
            if len(size_bytes) < 2:
                raise ValueError(f"Unexpected EOF reading size in {ips_path}")
            size = int.from_bytes(size_bytes, "big")
            if size == 0:
                rle_size_bytes = f.read(2)
                if len(rle_size_bytes) < 2:
                    raise ValueError(f"Unexpected EOF reading RLE size in {ips_path}")
                rle_size = int.from_bytes(rle_size_bytes, "big")
                value = f.read(1)
                if not value:
                    raise ValueError(f"Unexpected EOF reading RLE value in {ips_path}")
                ranges.append((offset, offset + rle_size))
            else:
                data = f.read(size)
                if len(data) < size:
                    raise ValueError(f"Unexpected EOF reading data block in {ips_path}")
                ranges.append((offset, offset + size))
    return ranges

def apply_ips_patch(rom_data: bytearray, ips_path: str):
    with open(ips_path, "rb") as f:
        header = f.read(5)
        if header != b"PATCH":
            raise ValueError(f"{ips_path} is not a valid IPS file")
        while True:
            offset_bytes = f.read(3)
            if not offset_bytes:
                raise ValueError(f"Unexpected EOF in IPS: {ips_path}")
            if offset_bytes == b"EOF":
                break
            offset = int.from_bytes(offset_bytes, "big")
            size = int.from_bytes(f.read(2), "big")
            if size == 0:
                rle_size = int.from_bytes(f.read(2), "big")
                value = f.read(1)
                if len(value) != 1:
                    raise ValueError(f"Unexpected EOF reading RLE value in {ips_path}")
                needed = offset + rle_size
                if needed > len(rom_data):
                    rom_data.extend(b"\x00" * (needed - len(rom_data)))
                rom_data[offset:offset + rle_size] = value * rle_size
            else:
                data = f.read(size)
                if len(data) < size:
                    raise ValueError(f"Unexpected EOF reading data block in {ips_path}")
                needed = offset + size
                if needed > len(rom_data):
                    rom_data.extend(b"\x00" * (needed - len(rom_data)))
                rom_data[offset:offset + size] = data
    return rom_data

def detect_conflicts_for_selection(patches_dir, patch_filenames):
    ownership = defaultdict(list)
    conflicts = []
    for patch in patch_filenames:
        path = os.path.join(patches_dir, patch)
        ranges = parse_ips_ranges(path)
        for start, end in ranges:
            if start < 0: continue
            for i in range(start, end):
                ownership[i].append(patch)
    for offset, writers in ownership.items():
        unique = sorted(set(writers))
        if len(unique) > 1:
            conflicts.append({"offset": offset, "patches": unique})
    return conflicts

def apply_patches_to_rom(base_rom_path, patches_dir, ordered_patch_list, output_rom_path, progress_callback=None):
    try:
        if progress_callback: progress_callback("Reading base ROM...")
        with open(base_rom_path, "rb") as f:
            rom_data = bytearray(f.read())
        for patch in ordered_patch_list:
            if progress_callback: progress_callback(f"Applying {patch}...")
            apply_ips_patch(rom_data, os.path.join(patches_dir, patch))
        if progress_callback: progress_callback(f"Writing output ROM to {output_rom_path}...")
        with open(output_rom_path, "wb") as out:
            out.write(rom_data)
        return True, f"Patched ROM written to {output_rom_path}"
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"Error applying patches: {e}\n{tb}"

# -------------------------------
# UI infrastructure
# -------------------------------
def log(msg: str):
    prev = dpg.get_value("log_text")
    new = prev + msg + "\n"
    dpg.set_value("log_text", new)

def refresh_patch_list_ui():
    # clear container children
    if dpg.does_item_exist("patch_list_child"):
        dpg.delete_item("patch_list_child", children_only=True)
    patches = APP_STATE.get("patches_order", [])
    for idx, patch in enumerate(patches):
        # build safe tags
        cb_tag = sanitize_tag(f"cb::{patch}")
        text_tag = sanitize_tag(f"text::{patch}")

        # default checkbox value True
        with dpg.group(parent="patch_list_child", horizontal=True):
            dpg.add_checkbox(label="", tag=cb_tag, default_value=True)
            dpg.add_text(patch, tag=text_tag)
            dpg.add_spacer(width=20)
            # DPG-style: pass user_data (patch filename). Callback signature: (sender, app_data, user_data)
            dpg.add_button(label="Up", width=50, callback=on_move_up_cb, user_data=patch)
            dpg.add_button(label="Down", width=50, callback=on_move_down_cb, user_data=patch)
            dpg.add_spacer(width=6)
            dpg.add_button(label="Info", width=50, callback=on_info_cb, user_data=patch)

def move_patch_up_by_name(patch_name):
    patches = APP_STATE["patches_order"]
    if patch_name not in patches: return
    idx = patches.index(patch_name)
    if idx <= 0: return
    patches[idx-1], patches[idx] = patches[idx], patches[idx-1]
    APP_STATE["patches_order"] = patches
    refresh_patch_list_ui()

def move_patch_down_by_name(patch_name):
    patches = APP_STATE["patches_order"]
    if patch_name not in patches: return
    idx = patches.index(patch_name)
    if idx >= len(patches)-1: return
    patches[idx+1], patches[idx] = patches[idx], patches[idx+1]
    APP_STATE["patches_order"] = patches
    refresh_patch_list_ui()

# DPG callback wrappers (use user_data)
def on_move_up_cb(sender, app_data, user_data):
    # user_data is patch filename
    move_patch_up_by_name(user_data)

def on_move_down_cb(sender, app_data, user_data):
    move_patch_down_by_name(user_data)

def on_info_cb(sender, app_data, user_data):
    patch = user_data
    patches_dir = APP_STATE.get("patches_dir")
    if not patches_dir:
        log("No patches folder set.")
        return
    path = os.path.join(patches_dir, patch)
    if not os.path.isfile(path):
        log(f"Patch file missing: {path}")
        return
    try:
        ranges = parse_ips_ranges(path)
        msg = f"{patch}:\nBlocks: {len(ranges)}\n"
        total_bytes = sum(end-start for start,end in ranges)
        msg += f"Total bytes written (sum of blocks): {total_bytes}\nRanges:\n"
        for start, end in ranges[:20]:
            msg += f"  0x{start:06X} - 0x{end-1:06X} ({end-start} bytes)\n"
        if len(ranges) > 20:
            msg += f"  ... (+{len(ranges)-20} more ranges)\n"
        log(msg)
    except Exception as e:
        log(f"Error reading patch {patch}: {e}")

def load_patches_from_folder():
    patches_dir = APP_STATE.get("patches_dir")
    if not patches_dir or not os.path.isdir(patches_dir):
        log("Invalid patches folder")
        APP_STATE["patches_order"] = []
        refresh_patch_list_ui()
        return
    items = sorted([p for p in os.listdir(patches_dir) if p.lower().endswith(".ips")])
    APP_STATE["patches_order"] = items
    refresh_patch_list_ui()
    log(f"Found {len(items)} patches in {patches_dir}")

# -------------------------------
# Callbacks & apply flow
# -------------------------------
def base_rom_selected(sender, app_data):
    try:
        path = app_data.get("file_path_name") or app_data.get("file_path") or app_data
        if isinstance(path, (list, tuple)): path = path[0]
        APP_STATE["base_rom"] = path
        dpg.set_value("label_base_rom", os.path.basename(path))
        log(f"Selected base ROM: {path}")
        crc, sha1 = compute_hashes(path)
        dpg.set_value("label_crc", crc)
        dpg.set_value("label_sha1", sha1)
        matched=False
        for name, hashes in KNOWN_ROMS.items():
            if crc == hashes["crc32"] and sha1 == hashes["sha1"]:
                dpg.set_value("label_rom_match", f"Detected: {name}")
                matched=True; break
        if not matched:
            dpg.set_value("label_rom_match", "Unknown ROM (warning)")
    except Exception as e:
        log(f"Error selecting base ROM: {e}")

def patches_folder_selected(sender, app_data):
    try:
        path = app_data.get("file_path_name") or app_data.get("file_path") or app_data
        if isinstance(path, (list, tuple)): path = path[0]
        if os.path.isfile(path): path = os.path.dirname(path)
        APP_STATE["patches_dir"] = path
        dpg.set_value("label_patches_dir", path)
        log(f"Selected patches folder: {path}")
        load_patches_from_folder()
    except Exception as e:
        log(f"Error selecting patches folder: {e}")

def detect_conflicts_button_cb():
    pd = APP_STATE.get("patches_dir")
    if not pd:
        log("Choose a patches folder first")
        return
    # build selected patches (respect current order)
    patches=[]
    for p in APP_STATE["patches_order"]:
        cb_tag = sanitize_tag(f"cb::{p}")
        try:
            include = dpg.get_value(cb_tag)
        except Exception:
            include = True
        if include: patches.append(p)
    if not patches:
        log("No patches selected for conflict check")
        return
    log(f"Running dry-run conflict detection for {len(patches)} patches...")
    try:
        conflicts = detect_conflicts_for_selection(pd, patches)
        if not conflicts:
            log("✓ No conflicts detected for selected patches")
        else:
            log(f"❌ {len(conflicts)} conflicting bytes found. Showing first 100 entries:")
            for c in conflicts[:100]:
                log(f"  Offset 0x{c['offset']:06X} written by: {', '.join(c['patches'])}")
            involved = set()
            for c in conflicts:
                involved.update(c["patches"])
            # mark checkboxes for involved patches by appending an asterisk to the text label
            for p in APP_STATE["patches_order"]:
                text_tag = sanitize_tag(f"text::{p}")
                if p in involved:
                    try:
                        if dpg.does_item_exist(text_tag):
                            cfg = dpg.get_item_configuration(text_tag)
                            orig_label = cfg.get("label") or cfg.get("default_value") or p
                            if not orig_label.endswith(" *"):
                                dpg.configure_item(text_tag, label=orig_label + " *")
                    except Exception:
                        pass
            log("Conflicting patches have been marked with an asterisk in the list. Consider reordering or excluding them.")
    except Exception as e:
        log(f"Error during conflict detection: {e}")

def choose_output_and_apply():
    if not APP_STATE.get("base_rom"):
        log("Select a base ROM first")
        return
    if not APP_STATE.get("patches_dir"):
        log("Select a patches folder first")
        return
    dpg.show_item("save_output_dialog")

def save_output_dialog_cb(sender, app_data):
    path = app_data.get("file_path_name") or app_data.get("file_path") or app_data
    if isinstance(path, (list, tuple)): path = path[0]
    if not path.lower().endswith(".gba"): path += ".gba"
    patches = []
    for p in APP_STATE["patches_order"]:
        cb_tag = sanitize_tag(f"cb::{p}")
        try:
            include = dpg.get_value(cb_tag)
        except Exception:
            include = True
        if include: patches.append(p)
    if not patches:
        log("No patches selected to apply")
        return
    conflicts = detect_conflicts_for_selection(APP_STATE["patches_dir"], patches)
    if conflicts:
        log("Conflicts detected — aborting apply. Resolve conflicts or deselect patches.")
        return
    log(f"Applying {len(patches)} patches to {APP_STATE['base_rom']} -> {path}")
    success, message = apply_patches_to_rom(APP_STATE["base_rom"], APP_STATE["patches_dir"], patches, path, progress_callback=log)
    if success:
        log("✓ Apply finished: " + message)
    else:
        log("❌ Apply failed: " + message)

# -------------------------------
# Build UI (auto-load patches dir if default exists)
# -------------------------------
def build_ui():
    dpg.create_context()
    with dpg.window(label="FireRed IPS Patcher", width=900, height=700):
        # Base ROM row
        with dpg.group(horizontal=True):
            dpg.add_text("Base ROM:")
            dpg.add_text("(none)", tag="label_base_rom")
            dpg.add_button(label="Choose ROM...", callback=lambda: dpg.show_item("base_rom_dialog"))

        dpg.add_spacing(count=1)

        # Hashes row
        with dpg.group(horizontal=True):
            dpg.add_text("CRC32:")
            dpg.add_text("", tag="label_crc")
            dpg.add_spacer(width=20)
            dpg.add_text("SHA1:")
            dpg.add_text("", tag="label_sha1")
            dpg.add_spacer(width=20)
            dpg.add_text("ROM match:")
            dpg.add_text("", tag="label_rom_match")

        dpg.add_separator()

        # Patches folder row
        with dpg.group(horizontal=True):
            dpg.add_text("Patches folder:")
            dpg.add_text("(none)", tag="label_patches_dir")
            dpg.add_button(label="Choose Patches Folder...", callback=lambda: dpg.show_item("patches_folder_dialog"))

        dpg.add_spacing(count=1)

        dpg.add_text("Patch list (use Up/Down to reorder; uncheck to exclude):")
        with dpg.child_window(tag="patch_list_child", width=860, height=260, autosize_y=False):
            pass

        # Controls
        with dpg.group(horizontal=True):
            dpg.add_button(label="Refresh list", callback=lambda: load_patches_from_folder())
            dpg.add_button(label="Detect Conflicts (dry-run)", callback=lambda s,a: detect_conflicts_button_cb())
            dpg.add_button(label="Choose output & Apply", callback=lambda s,a: choose_output_and_apply())

        dpg.add_separator()
        dpg.add_text("Log:")
        dpg.add_input_text(tag="log_text", default_value="", multiline=True, readonly=True, width=860, height=200)

    # file dialogs
    with dpg.file_dialog(directory_selector=False, show=False, callback=base_rom_selected, tag="base_rom_dialog"):
        dpg.add_file_extension(".gba")
        dpg.add_file_extension(".*")

    with dpg.file_dialog(directory_selector=True, show=False, callback=patches_folder_selected, tag="patches_folder_dialog"):
        pass

    with dpg.file_dialog(directory_selector=False, show=False, callback=save_output_dialog_cb, tag="save_output_dialog", default_filename="FireRed_patched.gba"):
        dpg.add_file_extension(".gba")

    # viewport
    dpg.create_viewport(title='FireRed IPS Patcher', width=920, height=740)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # if default patches dir exists, set UI label and load it
    if APP_STATE.get("patches_dir"):
        dpg.set_value("label_patches_dir", APP_STATE["patches_dir"])
        load_patches_from_folder()

    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    build_ui()
