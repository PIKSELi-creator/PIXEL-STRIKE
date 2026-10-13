from pathlib import Path

root = Path(__file__).resolve().parent

dirs = [
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    "Assets/Scenes",
    "Assets/Scripts/Core",
    "Assets/Scripts/Player",
    "Assets/Scripts/Camera",
    "Assets/Scripts/Weapons/Definitions",
    "Assets/Scripts/Combat",
    "Assets/Scripts/AI",
    "Assets/Scripts/GameModes",
    "Assets/Scripts/Maps",
    "Assets/Scripts/UI",
    "Assets/Scripts/Mobile",
    "Assets/Scripts/Audio",
    "Assets/Scripts/Settings",
    "Assets/Scripts/Performance",
    "Assets/Scripts/Multiplayer",
    "Assets/Scripts/Utilities",
    "Assets/Art/Splash",
    "Assets/Art/Logo",
    "Assets/Art/Characters/Player",
    "Assets/Art/Characters/Bots",
    "Assets/Art/Weapons/AKR",
    "Assets/Art/Weapons/Glock",
    "Assets/Art/Weapons/Knife",
    "Assets/Art/Maps/MainArena",
    "Assets/Art/Environment/Crates",
    "Assets/Art/Environment/Barrels",
    "Assets/Art/Environment/Props",
    "Assets/Art/Materials",
    "Assets/Art/Textures",
    "Assets/Art/Icons",
    "Assets/Art/Fonts",
    "Assets/Audio/Music",
    "Assets/Audio/Weapons",
    "Assets/Audio/Movement",
    "Assets/Audio/UI",
    "Assets/Audio/Environment",
    "Assets/Prefabs/Player",
    "Assets/Prefabs/Bots",
    "Assets/Prefabs/Weapons",
    "Assets/Prefabs/UI",
    "Assets/Prefabs/Effects",
    "Assets/Prefabs/Environment",
    "Assets/Data/Weapons",
    "Assets/Data/GameModes",
    "Assets/Data/Maps",
    "Assets/Data/Graphics",
    "Assets/Resources",
    "Assets/Editor",
    "Assets/Tests/EditMode",
    "Assets/Tests/PlayMode",
    "Assets/Settings",
    "Packages",
    "ProjectSettings",
    "Build",
    "Documentation",
    "Tools",
]

scripts = {
    "Core": [
        "GameBootstrap", "GameManager", "SceneLoader", "GameState",
        "GameSettings", "ServiceLocator", "ApplicationLifecycle"
    ],
    "Player": [
        "PlayerController", "PlayerMovement", "PlayerLook", "PlayerHealth",
        "PlayerAnimation", "PlayerEquipment", "PlayerRespawn",
        "PlayerInputHandler"
    ],
    "Camera": [
        "FPSCameraController", "CameraShake", "RecoilCamera",
        "CameraSensitivity"
    ],
    "Weapons": [
        "WeaponBase", "WeaponController", "WeaponData", "WeaponInventory",
        "WeaponSwitching", "WeaponRecoil", "WeaponSway", "WeaponReload",
        "WeaponEffects", "Projectile", "HitscanSystem", "Ammunition"
    ],
    "Weapons/Definitions": ["AKRWeapon", "GlockWeapon", "KnifeWeapon"],
    "Combat": [
        "DamageInfo", "DamageSystem", "HitDetection", "HitMarker",
        "HeadshotDetection", "KillTracker"
    ],
    "AI": [
        "BotController", "BotMovement", "BotCombat",
        "BotPerception", "BotHealth", "BotSpawner"
    ],
    "GameModes": [
        "GameModeBase", "TeamDeathmatch", "BombMode",
        "RoundManager", "MatchTimer", "ScoreManager"
    ],
    "Maps": ["MapManager", "SpawnPoint", "TeamSpawnManager", "MapBounds"],
    "UI": [
        "MainMenuController", "PauseMenu", "HUDController",
        "HealthDisplay", "AmmoDisplay", "CrosshairController",
        "ScoreboardController", "SettingsMenu", "LoadingScreenController",
        "StudioIntroController", "MatchResultScreen", "NotificationController"
    ],
    "Mobile": [
        "MobileInputManager", "VirtualJoystick", "TouchLookController",
        "FireButton", "AimButton", "ReloadButton", "JumpButton",
        "CrouchButton", "MobileLayoutManager"
    ],
    "Audio": ["AudioManager", "MusicManager", "WeaponAudio", "SpatialAudio"],
    "Settings": [
        "GraphicsSettings", "AudioSettings", "ControlSettings",
        "SettingsStorage"
    ],
    "Performance": [
        "QualityManager", "DeviceCapabilities",
        "FrameRateController", "ObjectPool"
    ],
    "Multiplayer": [
        "NetworkBootstrap", "NetworkPlayer", "NetworkMatchManager",
        "LobbyManager", "NetworkSettings"
    ],
    "Utilities": [
        "Singleton", "TimerUtility", "LayerConstants", "DebugLogger"
    ],
}

for directory in dirs:
    (root / directory).mkdir(parents=True, exist_ok=True)

created = 0
for folder, names in scripts.items():
    for name in names:
        path = root / "Assets" / "Scripts" / folder / f"{name}.cs"
        if path.exists():
            continue
        path.write_text(
            "using UnityEngine;\n\n"
            f"public class {name} : MonoBehaviour\n"
            "{\n"
            "    // TODO: Implement this system.\n"
            "}\n",
            encoding="utf-8"
        )
        created += 1

scene_names = [
    "Boot", "StudioIntro", "LoadingScreen", "MainMenu",
    "Lobby", "Training", "MainArena", "TestRange"
]
for name in scene_names:
    (root / "Assets" / "Scenes" / f"{name}.README.md").write_text(
        f"# {name}\n\nUnity scene planned for PIXEL STRIKE.\n"
        "Create and configure this scene in a compatible Unity Editor/build pipeline.\n",
        encoding="utf-8"
    )

docs = {
    "GAME_DESIGN.md": "# PIXEL STRIKE — Game Design\n\nMobile 3D FPS for Android.\n",
    "ARCHITECTURE.md": "# Architecture\n\nC# gameplay systems organized by responsibility.\n",
    "BUILD_ANDROID.md": "# Android Build\n\nUnity Android build and GitHub Actions setup.\n",
    "CONTROLS.md": "# Controls\n\nTouch joystick, look, fire, aim, reload and crouch.\n",
    "ASSET_LICENSES.md": "# Asset Licenses\n\nRecord the source and license of every third-party asset.\n",
    "ROADMAP.md": "# Roadmap\n\n1. Boot and loading screen\n2. FPS movement\n3. Weapon system\n4. Bots and maps\n5. Android build\n6. Multiplayer research\n",
}
for name, content in docs.items():
    path = root / "Documentation" / name
    if not path.exists():
        path.write_text(content, encoding="utf-8")

readme = root / "README.md"
if not readme.exists():
    readme.write_text(
        "# PIXEL STRIKE\n\n"
        "A mobile 3D FPS project built with C# and Unity.\n\n"
        "## Status\n\n"
        "Project scaffolding only. Gameplay and Unity scenes are not yet implemented.\n",
        encoding="utf-8"
    )

gitignore = root / ".gitignore"
if not gitignore.exists():
    gitignore.write_text(
        "Library/\nTemp/\nObj/\nBuilds/\nLogs/\nUserSettings/\n"
        ".vs/\n.vscode/\n*.csproj\n*.sln\n*.apk\n*.aab\n",
        encoding="utf-8"
    )

(root / "Build" / "README.md").write_text(
    "# Build Output\n\nGenerated builds should not be committed here.\n",
    encoding="utf-8"
)

(root / "Tools" / "README.md").write_text(
    "# Tools\n\nPhone-friendly project maintenance scripts.\n",
    encoding="utf-8"
)

print("PIXEL STRIKE structure created.")
print(f"New C# scripts: {created}")
print(f"Directories prepared: {len(dirs)}")
print("Note: generated C# files are placeholders, not finished gameplay.")
