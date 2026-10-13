using UnityEngine;

namespace PixelStrike.Settings
{
    public sealed class GraphicsSettingsController : MonoBehaviour
    {
        private const string QualityKey = "PS_Quality";

        private void Start()
        {
            int saved = PlayerPrefs.GetInt(QualityKey, 1);
            ApplyQuality(saved);
        }

        public void ApplyQuality(int index)
        {
            if (QualitySettings.names.Length == 0) return;

            index = Mathf.Clamp(index, 0, QualitySettings.names.Length - 1);
            QualitySettings.SetQualityLevel(index, true);
            PlayerPrefs.SetInt(QualityKey, index);
            PlayerPrefs.Save();
        }

        public void SetLow() => ApplyQuality(0);
        public void SetMedium() => ApplyQuality(
            Mathf.Min(1, QualitySettings.names.Length - 1));
        public void SetHigh() => ApplyQuality(
            Mathf.Max(0, QualitySettings.names.Length - 1));
    }
}
