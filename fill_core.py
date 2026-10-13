from pathlib import Path

root = Path("Assets/Scripts/Core")
root.mkdir(parents=True, exist_ok=True)

files = {
"GameState.cs": r'''
public enum GameState
{
    Boot,
    StudioIntro,
    Loading,
    MainMenu,
    Lobby,
    Playing,
    Paused,
    Results
}
''',

"GameSettings.cs": r'''
using UnityEngine;

public static class GameSettings
{
    private const string MusicKey = "music_volume";
    private const string SfxKey = "sfx_volume";
    private const string SensitivityKey = "look_sensitivity";
    private const string QualityKey = "graphics_quality";

    public static float MusicVolume
    {
        get => PlayerPrefs.GetFloat(MusicKey, 0.8f);
        set => PlayerPrefs.SetFloat(MusicKey, Mathf.Clamp01(value));
    }

    public static float SfxVolume
    {
        get => PlayerPrefs.GetFloat(SfxKey, 1f);
        set => PlayerPrefs.SetFloat(SfxKey, Mathf.Clamp01(value));
    }

    public static float LookSensitivity
    {
        get => PlayerPrefs.GetFloat(SensitivityKey, 1f);
        set => PlayerPrefs.SetFloat(
            SensitivityKey, Mathf.Clamp(value, 0.1f, 5f));
    }

    public static int GraphicsQuality
    {
        get => PlayerPrefs.GetInt(QualityKey, 1);
        set => PlayerPrefs.SetInt(QualityKey, Mathf.Clamp(value, 0, 2));
    }

    public static void Save()
    {
        PlayerPrefs.Save();
    }
}
''',

"GameManager.cs": r'''
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    public GameState CurrentState { get; private set; } = GameState.Boot;

    public event System.Action<GameState> StateChanged;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        DontDestroyOnLoad(gameObject);
        Application.targetFrameRate = 60;
        Screen.sleepTimeout = SleepTimeout.Never;
    }

    public bool SetState(GameState nextState)
    {
        if (CurrentState == nextState)
            return false;

        CurrentState = nextState;
        StateChanged?.Invoke(nextState);
        Debug.Log($"[PIXEL STRIKE] State: {nextState}");
        return true;
    }

    private void OnDestroy()
    {
        if (Instance == this)
            Instance = null;
    }
}
''',

"GameBootstrap.cs": r'''
using UnityEngine;

public class GameBootstrap : MonoBehaviour
{
    [SerializeField] private string firstScene = "StudioIntro";

    private void Awake()
    {
        Application.targetFrameRate = 60;
        QualitySettings.vSyncCount = 0;

        if (GameManager.Instance == null)
        {
            GameObject managerObject = new GameObject("GameManager");
            managerObject.AddComponent<GameManager>();
        }

        Debug.Log("[PIXEL STRIKE] Bootstrap initialized.");

        if (!string.IsNullOrWhiteSpace(firstScene))
            SceneLoader.Load(firstScene);
    }
}
''',

"SceneLoader.cs": r'''
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;

public static class SceneLoader
{
    private static bool isLoading;

    public static void Load(string sceneName)
    {
        if (string.IsNullOrWhiteSpace(sceneName))
        {
            Debug.LogError("[PIXEL STRIKE] Scene name is empty.");
            return;
        }

        if (isLoading)
        {
            Debug.LogWarning("[PIXEL STRIKE] A scene is already loading.");
            return;
        }

        GameManager.Instance?.SetState(GameState.Loading);

        var runner = SceneLoadRunner.Instance;
        if (runner == null)
        {
            var go = new GameObject("SceneLoadRunner");
            runner = go.AddComponent<SceneLoadRunner>();
        }

        runner.BeginLoad(sceneName);
    }

    public static void SetLoading(bool value)
    {
        isLoading = value;
    }
}

public class SceneLoadRunner : MonoBehaviour
{
    public static SceneLoadRunner Instance { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void BeginLoad(string sceneName)
    {
        StartCoroutine(LoadRoutine(sceneName));
    }

    private IEnumerator LoadRoutine(string sceneName)
    {
        SceneLoader.SetLoading(true);

        AsyncOperation operation = SceneManager.LoadSceneAsync(sceneName);

        if (operation == null)
        {
            Debug.LogError(
                $"[PIXEL STRIKE] Cannot load scene '{sceneName}'. " +
                "Check that it exists and is included in the build settings.");
            SceneLoader.SetLoading(false);
            yield break;
        }

        while (!operation.isDone)
            yield return null;

        SceneLoader.SetLoading(false);
    }

    private void OnDestroy()
    {
        if (Instance == this)
            Instance = null;
    }
}
''',

"ServiceLocator.cs": r'''
using System;
using System.Collections.Generic;

public static class ServiceLocator
{
    private static readonly Dictionary<Type, object> Services = new();

    public static void Register<T>(T service) where T : class
    {
        if (service == null)
            throw new ArgumentNullException(nameof(service));

        Services[typeof(T)] = service;
    }

    public static bool TryGet<T>(out T service) where T : class
    {
        if (Services.TryGetValue(typeof(T), out object value))
        {
            service = value as T;
            return service != null;
        }

        service = null;
        return false;
    }

    public static T Get<T>() where T : class
    {
        if (TryGet<T>(out T service))
            return service;

        throw new InvalidOperationException(
            $"Service {typeof(T).Name} has not been registered.");
    }

    public static void Unregister<T>() where T : class
    {
        Services.Remove(typeof(T));
    }

    public static void Clear()
    {
        Services.Clear();
    }
}
''',

"ApplicationLifecycle.cs": r'''
using UnityEngine;

public class ApplicationLifecycle : MonoBehaviour
{
    private void OnApplicationPause(bool paused)
    {
        if (paused)
        {
            GameSettings.Save();
            Debug.Log("[PIXEL STRIKE] Application paused.");
        }
    }

    private void OnApplicationQuit()
    {
        GameSettings.Save();
        Debug.Log("[PIXEL STRIKE] Settings saved.");
    }
}
'''
}

for name, content in files.items():
    path = root / name
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("Updated:", path)

print(f"\nDone. Updated {len(files)} Core files.")
print("Unity scenes and project settings are still required to run the game.")
