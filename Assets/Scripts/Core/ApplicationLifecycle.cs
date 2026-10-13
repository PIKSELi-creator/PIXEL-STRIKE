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
