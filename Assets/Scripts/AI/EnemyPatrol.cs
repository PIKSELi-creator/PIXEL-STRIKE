using UnityEngine;

namespace PixelStrike.AI
{
    public sealed class EnemyPatrol : MonoBehaviour
    {
        [SerializeField] private Transform[] points;
        [SerializeField] private float speed = 2f;
        [SerializeField] private float reachDistance = 0.2f;
        private int currentPoint;

        private void Update()
        {
            if (points == null || points.Length == 0 ||
                points[currentPoint] == null)
                return;

            Transform target = points[currentPoint];
            transform.position = Vector3.MoveTowards(
                transform.position, target.position, speed * Time.deltaTime);

            Vector3 direction = target.position - transform.position;
            direction.y = 0f;

            if (direction.sqrMagnitude > 0.01f)
                transform.rotation = Quaternion.Slerp(
                    transform.rotation,
                    Quaternion.LookRotation(direction),
                    5f * Time.deltaTime);

            if (Vector3.Distance(transform.position, target.position) <= reachDistance)
                currentPoint = (currentPoint + 1) % points.Length;
        }
    }
}
