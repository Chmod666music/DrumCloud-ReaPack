-- @noindex
-- DrumCloud JS v0.23 factory preset installer

local resource_path = reaper.GetResourcePath()
local separator = package.config:sub(1, 1)
local source_path = table.concat({resource_path, "Data", "DrumCloud", "DrumCloud_v0.23_46_Factory_Presets.ini"}, separator)
local preset_dir = table.concat({resource_path, "presets"}, separator)
local target_path = table.concat({preset_dir, "js-DrumCloud_JS_DrumCloud_JS_jsfx.ini"}, separator)

local function read_file(path)
  local file = io.open(path, "rb")
  if not file then return nil end
  local contents = file:read("*a")
  file:close()
  return contents
end

local function write_file(path, contents)
  local file = io.open(path, "wb")
  if not file then return false end
  file:write(contents)
  file:close()
  return true
end

local factory_presets = read_file(source_path)
if not factory_presets then
  reaper.ShowMessageBox(
    "The DrumCloud factory preset file was not found.\n\nReinstall DrumCloud JS with ReaPack, then run this action again.",
    "DrumCloud JS",
    0
  )
  return
end

if not factory_presets:find("NbPresets=46", 1, true) then
  reaper.ShowMessageBox("The factory preset file is incomplete or invalid.", "DrumCloud JS", 0)
  return
end

local existing_presets = read_file(target_path)
if existing_presets == factory_presets then
  reaper.ShowMessageBox("The 46 DrumCloud factory presets are already installed.", "DrumCloud JS", 0)
  return
end

local message = "Install the 46 DrumCloud v0.23 factory presets?"
if existing_presets then
  message = message .. "\n\nYour current DrumCloud preset bank will be backed up first."
end

if reaper.ShowMessageBox(message, "DrumCloud JS", 1) ~= 1 then return end

reaper.RecursiveCreateDirectory(preset_dir, 0)

if existing_presets then
  local backup_path = target_path .. ".backup-" .. os.date("%Y%m%d-%H%M%S")
  if not write_file(backup_path, existing_presets) then
    reaper.ShowMessageBox("Could not create a backup of the current preset bank. Nothing was changed.", "DrumCloud JS", 0)
    return
  end
end

if not write_file(target_path, factory_presets) then
  reaper.ShowMessageBox("Could not write the DrumCloud preset bank.", "DrumCloud JS", 0)
  return
end

reaper.ShowMessageBox(
  "Installed all 46 DrumCloud v0.23 factory presets.\n\nClose and reopen DrumCloud JS to refresh the preset list.",
  "DrumCloud JS",
  0
)
