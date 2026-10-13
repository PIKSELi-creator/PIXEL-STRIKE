using UnityEngine;

namespace PixelStrike.AI
{
    public sealed class EnemyTarget : MonoBehaviour
    {
        [SerializeField] private Transform target;
        [SerializeField] private float detectionRange = 20f;
        [SerializeField] private float turnSpeed = 4f;

        public Transform Target => target;
        public bool HasTarget =>
            target != null &&
            Vector3.Distance(transform.position, target.position) <= detectionRange;

        public void SetTarget(Transform newTarget) => target = newTarget;

        private void Update()
        {
            if (!HasTarget) return;

            Vector3 direction = target.position - transform.position;
            direction.y = 0f;
            if (direction.sqrMagnitude < 0.001f) return;

            Quaternion look = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(
                transform.rotation, look, turnSpeed * Time.deltaTime);
        }
    }
}
