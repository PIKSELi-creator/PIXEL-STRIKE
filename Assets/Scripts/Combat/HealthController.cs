
using System;
using UnityEngine;

namespace PixelStrike.Combat
{
    public sealed class HealthController : MonoBehaviour,
        PixelStrike.Weapons.IDamageable
    {
        [Header("Здоровье")]
        [SerializeField, Min(1)] private int maxHealth = 100;

        [Header("Поведение")]
        [SerializeField] private bool destroyOnDeath = true;
        [SerializeField, Min(0f)] private float destroyDelay = 0.1f;

        public int MaxHealth => maxHealth;
        public int CurrentHealth { get; private set; }
        public bool IsDead { get; private set; }

        public event Action<int, int> HealthChanged;
        public event Action Died;

        private void Awake()
        {
            CurrentHealth = maxHealth;
        }

        public void TakeDamage(int amount)
        {
            if (IsDead || amount <= 0)
                return;

            CurrentHealth = Mathf.Max(0, CurrentHealth - amount);
            HealthChanged?.Invoke(CurrentHealth, maxHealth);

            if (CurrentHealth == 0)
                Die();
        }

        public void Heal(int amount)
        {
            if (IsDead || amount <= 0)
                return;

            int previousHealth = CurrentHealth;
            CurrentHealth = Mathf.Min(maxHealth, CurrentHealth + amount);

            if (CurrentHealth != previousHealth)
                HealthChanged?.Invoke(CurrentHealth, maxHealth);
        }

        public void ResetHealth()
        {
            IsDead = false;
            CurrentHealth = maxHealth;
            HealthChanged?.Invoke(CurrentHealth, maxHealth);
        }

        private void Die()
        {
            if (IsDead)
                return;

            IsDead = true;
            Died?.Invoke();

            if (destroyOnDeath)
                Destroy(gameObject, destroyDelay);
        }
    }
}

