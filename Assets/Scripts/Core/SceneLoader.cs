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
