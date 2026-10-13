
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace PixelStrike.UI
{
    public sealed class LoadingScreenController : MonoBehaviour
    {
        [Header("Сцена")]
        [SerializeField] private string nextSceneName = "MainMenu";

        [Header("Элементы интерфейса")]
        [SerializeField] private Slider progressBar;
        [SerializeField] private Text progressText;
        [SerializeField] private Text statusText;

        [Header("Настройки")]
        [SerializeField, Min(0f)] private float minimumDisplayTime = 2f;

        private IEnumerator Start()
        {
            if (progressBar != null)
                progressBar.value = 0f;

            if (progressText != null)
                progressText.text = "0%";

            if (statusText != null)
                statusText.text = "Подготовка игры...";

            float startTime = Time.unscaledTime;

            yield return null;

            if (string.IsNullOrWhiteSpace(nextSceneName))
            {
                Debug.LogError(
                    "PIXEL STRIKE: не указано имя следующей сцены."
                );
                yield break;
            }

            AsyncOperation operation =
                SceneManager.LoadSceneAsync(nextSceneName);

            if (operation == null)
            {
                Debug.LogError(
                    "PIXEL STRIKE: не удалось загрузить сцену " +
                    nextSceneName
                );
                yield break;
            }

            operation.allowSceneActivation = false;

            while (operation.progress < 0.9f)
            {
                UpdateProgress(operation.progress / 0.9f);
                yield return null;
            }

            UpdateProgress(1f);

            if (statusText != null)
                statusText.text = "Готово!";

            float remainingTime =
                minimumDisplayTime - (Time.unscaledTime - startTime);

            if (remainingTime > 0f)
                yield return new WaitForSecondsRealtime(remainingTime);

            operation.allowSceneActivation = true;
        }

        private void UpdateProgress(float value)
        {
            value = Mathf.Clamp01(value);

            if (progressBar != null)
                progressBar.value = value;

            if (progressText != null)
                progressText.text =
                    Mathf.RoundToInt(value * 100f) + "%";

            if (statusText != null && value < 1f)
                statusText.text = "Загрузка ресурсов...";
        }
    }
}

