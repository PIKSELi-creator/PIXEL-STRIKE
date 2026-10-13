
using UnityEngine;
using PixelStrike.Combat;

namespace PixelStrike.AI
{
    [RequireComponent(typeof(HealthController))]
    public sealed class EnemyController : MonoBehaviour
    {
        [Header("Настройки противника")]
        [SerializeField] private string enemyName = "Training Bot";
        [SerializeField] private bool logDeath = true;

        private HealthController health;

        private void Awake()
        {
            health = GetComponent<HealthController>();
            health.Died += OnDied;
        }

        private void OnDestroy()
        {
            if (health != null)
                health.Died -= OnDied;
        }

        private void OnDied()
        {
            if (logDeath)
                Debug.Log(enemyName + " уничтожен.");
        }
    }
}

