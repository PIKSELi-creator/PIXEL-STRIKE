
using UnityEngine;
using UnityEngine.SceneManagement;

namespace PixelStrike.UI
{
    public sealed class MainMenuController : MonoBehaviour
    {
        [Header("Названия сцен")]
        [SerializeField] private string gameSceneName = "Game";
        [SerializeField] private string weaponsSceneName = "Weapons";
        [SerializeField] private string settingsSceneName = "Settings";

        public void PlayGame()
        {
            LoadScene(gameSceneName);
        }

        public void OpenWeapons()
        {
            LoadScene(weaponsSceneName);
        }

        public void OpenSettings()
        {
            LoadScene(settingsSceneName);
        }

        public void QuitGame()
        {
#if UNITY_EDITOR
            Debug.Log("PIXEL STRIKE: выход из игры в редакторе.");
#else
            Application.Quit();
#endif
        }

        private void LoadScene(string sceneName)
        {
            if (string.IsNullOrWhiteSpace(sceneName))
            {
                Debug.LogError(
                    "PIXEL STRIKE: имя сцены не задано."
                );
                return;
            }

            if (!Application.CanStreamedLevelBeLoaded(sceneName))
            {
                Debug.LogWarning(
                    "PIXEL STRIKE: сцена '" + sceneName +
                    "' ещё не добавлена в настройки сборки."
                );
                return;
            }

            SceneManager.LoadSceneAsync(sceneName);
        }
    }
}
	
