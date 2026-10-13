using UnityEngine;

namespace PixelStrike.Weapons
{
    [CreateAssetMenu(fileName = "WeaponDefinition", menuName = "PIXEL STRIKE/Weapon")]
    public sealed class WeaponDefinition : ScriptableObject
    {
        public string weaponName = "AKR";
        [Min(1)] public int damage = 25;
        [Min(1)] public int magazineSize = 30;
        [Min(0.05f)] public float shotsPerSecond = 10f;
        [Min(1f)] public float range = 100f;
        [Min(0f)] public float reloadSeconds = 2f;
        [Min(0f)] public float recoil = 1f;
        public bool automatic = true;
    }
}
