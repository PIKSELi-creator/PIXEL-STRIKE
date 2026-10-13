using UnityEngine;

namespace PixelStrike.Player
{
    public sealed class PlayerSpawnPoint : MonoBehaviour
    {
        [SerializeField] private bool drawGizmo = true;

        public Vector3 Position => transform.position;
        public Quaternion Rotation => transform.rotation;

        private void OnDrawGizmos()
        {
            if (!drawGizmo) return;
            Gizmos.color = Color.cyan;
            Gizmos.DrawWireSphere(transform.position, 0.35f);
            Gizmos.DrawRay(transform.position, transform.forward * 1.5f);
        }
    }
}
