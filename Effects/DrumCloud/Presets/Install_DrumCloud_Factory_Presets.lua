-- @noindex
-- DrumCloud JS v0.23 factory preset installer

local resource_path = reaper.GetResourcePath()
local separator = package.config:sub(1, 1)
local source_path = table.concat({resource_path, "Data", "DrumCloud", "DrumCloud_v0.23_46_Factory_Presets.ini"}, separator)
local preset_dir = table.concat({resource_path, "presets"}, separator)
local effects_dir = table.concat({resource_path, "Effects"}, separator)

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

local function find_drumcloud_effects(directory, relative_directory, results)
  local file_index = 0
  while true do
    local filename = reaper.EnumerateFiles(directory, file_index)
    if not filename then break end
    if filename == "DrumCloud_JS.jsfx" then
      local relative_path = relative_directory == "" and filename
        or relative_directory .. separator .. filename
      results[#results + 1] = relative_path
    end
    file_index = file_index + 1
  end

  local directory_index = 0
  while true do
    local child_name = reaper.EnumerateSubdirectories(directory, directory_index)
    if not child_name then break end
    local child_path = directory .. separator .. child_name
    local child_relative = relative_directory == "" and child_name
      or relative_directory .. separator .. child_name
    find_drumcloud_effects(child_path, child_relative, results)
    directory_index = directory_index + 1
  end
end

local function preset_filename(effect_relative_path)
  local normalized = effect_relative_path:gsub("[\\/]", "_"):gsub("%.", "_")
  return "js-" .. normalized .. ".ini"
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

local effects = {}
find_drumcloud_effects(effects_dir, "", effects)

if #effects == 0 then
  reaper.ShowMessageBox(
    "DrumCloud_JS.jsfx was not found in the REAPER Effects directory.\n\nInstall DrumCloud JS with ReaPack, then run this action again.",
    "DrumCloud JS",
    0
  )
  return
end

local targets = {}
local already_installed = 0
local existing_count = 0

for _, effect_path in ipairs(effects) do
  local target_path = preset_dir .. separator .. preset_filename(effect_path)
  local existing_presets = read_file(target_path)
  targets[#targets + 1] = {
    effect_path = effect_path,
    target_path = target_path,
    existing_presets = existing_presets
  }
  if existing_presets == factory_presets then already_installed = already_installed + 1 end
  if existing_presets and existing_presets ~= factory_presets then existing_count = existing_count + 1 end
end

if already_installed == #targets then
  reaper.ShowMessageBox("The 46 DrumCloud factory presets are already installed.", "DrumCloud JS", 0)
  return
end

local message = "Install the 46 DrumCloud v0.23 factory presets?"
if #targets > 1 then
  message = message .. "\n\n" .. #targets .. " DrumCloud installations were found; presets will be installed for each one."
end
if existing_count > 0 then
  message = message .. "\n\nExisting DrumCloud preset banks will be backed up first."
end

if reaper.ShowMessageBox(message, "DrumCloud JS", 1) ~= 1 then return end

reaper.RecursiveCreateDirectory(preset_dir, 0)

for _, target in ipairs(targets) do
  if target.existing_presets ~= factory_presets then
    if target.existing_presets then
      local backup_path = target.target_path .. ".backup-" .. os.date("%Y%m%d-%H%M%S")
      if not write_file(backup_path, target.existing_presets) then
        reaper.ShowMessageBox("Could not create a backup for:\n" .. target.effect_path .. "\n\nNothing was changed for this installation.", "DrumCloud JS", 0)
        return
      end
    end

    if not write_file(target.target_path, factory_presets) then
      reaper.ShowMessageBox("Could not write the preset bank for:\n" .. target.effect_path, "DrumCloud JS", 0)
      return
    end
  end
end

reaper.ShowMessageBox(
  "Installed all 46 DrumCloud v0.23 factory presets.\n\nClose and reopen DrumCloud JS to refresh the preset list.",
  "DrumCloud JS",
  0
)
