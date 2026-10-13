
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace PixelStrike.UI
{
    public sealed class StudioIntroController : MonoBehaviour
    {
        [Header("Настройки заставки")]
        [SerializeField] private string nextSceneName = "SplashScreen";
        [SerializeField, Min(0f)] private float showDuration = 2.5f;

        [Header("Необязательно")]
        [SerializeField] private CanvasGroup logoCanvasGroup;
        [SerializeField] private Image backgroundImage;

        private bool isTransitioning;

        private IEnumerator Start()
        {
            if (logoCanvasGroup != null)
            {
                logoCanvasGroup.alpha = 0f;
                yield return Fade(0f, 1f, 0.5f);
            }

            float elapsed = 0f;

            while (elapsed < showDuration && !isTransitioning)
            {
                elapsed += Time.unscaledDeltaTime;

                if (Input.GetMouseButtonDown(0) ||
                    Input.touchCount > 0)
                {
                    break;
                }

                yield return null;
            }

            yield return LoadNextScene();
        }

        private IEnumerator Fade(float from, float to, float duration)
        {
            if (logoCanvasGroup == null)
                yield break;

            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.unscaledDeltaTime;
                logoCanvasGroup.alpha = Mathf.Lerp(
                    from,
                    to,
                    Mathf.Clamp01(elapsed / duration)
                );

                yield return null;
            }

            logoCanvasGroup.alpha = to;
        }

        private IEnumerator LoadNextScene()
        {
            if (isTransitioning)
                yield break;

            isTransitioning = true;

            if (logoCanvasGroup != null)
                yield return Fade(logoCanvasGroup.alpha, 0f, 0.25f);

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

            while (!operation.isDone)
                yield return null;
        }
    }
}

