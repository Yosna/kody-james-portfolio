#Include memory.ahk
#Include json.ahk

SaveSettings(game) {
    if !DirExist(game.directory) {
        DirCreate(game.directory)
    }

    local character := EncodeHex(JSON.stringify(GetCharacter(game)))
    local entry := character . "=" . game.deathsOffset
    local counters := ""

    for line in StrSplit(FileRead(game.settings), "`n") {
        line := Trim(line, "`r`n`t")

        if SubStr(line, 1, 1) = "[" || line == "" {
            continue ; skip keys and empty lines
        }

        local hex := StrSplit(line, "=")[1]
        
        if hex == character || hex == game.loadedHex {
            continue ; skip duplicates and the current loaded character
        } 

        counters .= line . "`n"
    }
    
    ; append the current character if there's an offset to save
    if game.deathsOffset != 0 {
        counters .= entry . "`n"
        game.deathsTotal := RetrieveMemory(game, game.offsets.deaths)
        game.loadedHex := character
    }

    IniDelete(game.settings, "Counters")
    IniWrite(counters, game.settings, "Counters")
}

LoadSettings(game) {
    if !DirExist(game.directory) {
        DirCreate(game.directory)
    }

    if !FileExist(game.settings) {
        return
    }

    local character := EncodeHex(JSON.stringify(GetCharacter(game)))

    for line in StrSplit(FileRead(game.settings), "`n") {
        line := Trim(line, "`r`n`t")

        if SubStr(line, 1, 1) = "[" || line == "" {
            continue ; skip keys and empty lines
        }

        local hex := StrSplit(line, "=")[1]

        if hex == character {
            game.deathsOffset := StrSplit(line, "=")[2]
            game.loadedHex := character
            break ; stop if a character is found
        }
    }
}

ReloadSettings(game, overlay) {
    game.deathsOffset := 0
    game.loadedHex := 0
    overlay.deaths.Value := "Deaths: 0"

    WaitForCharacterToLoad(game)
    LoadSettings(game)
}

GetCharacter(game) {
    return {
        name: RetrieveMemory(game, game.offsets.character),
        level: RetrieveMemory(game, game.offsets.level),
        runes: RetrieveMemory(game, game.offsets.runes),
        soulsmemory: RetrieveMemory(game, game.offsets.soulsmemory),
        deaths: RetrieveMemory(game, game.offsets.deaths),
    }
}

EncodeHex(data) {
    local result := ""

    for _, char in StrSplit(data) {
        result .= Format("{:02X}", Ord(char))
    }

    return result
}

WaitForCharacterToLoad(game) {
    While !RetrieveMemory(game, game.offsets.character) {
        Sleep(TICK_INTERVAL)
    }
}
