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
