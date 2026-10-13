using UnityEngine;
using UnityEngine.UI;
using PixelStrike.Combat;

namespace PixelStrike.UI
{
    public sealed class HealthHUD : MonoBehaviour
    {
        [SerializeField] private HealthController health;
        [SerializeField] private Slider healthBar;
        [SerializeField] private Text healthText;

        private void OnEnable()
        {
            if (health != null) health.HealthChanged += UpdateHealth;
        }

        private void OnDisable()
        {
            if (health != null) health.HealthChanged -= UpdateHealth;
        }

        private void Start()
        {
            if (health != null)
                UpdateHealth(health.CurrentHealth, health.MaxHealth);
        }

        private void UpdateHealth(int current, int maximum)
        {
            if (healthBar != null)
                healthBar.value = maximum > 0 ? (float)current / maximum : 0f;

            if (healthText != null)
                healthText.text = current + " HP";
        }
    }
}
