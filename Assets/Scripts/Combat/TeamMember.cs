using UnityEngine;

namespace PixelStrike.Combat
{
    public enum TeamId { Neutral, Alpha, Bravo }

    public sealed class TeamMember : MonoBehaviour
    {
        [SerializeField] private TeamId team = TeamId.Neutral;
        public TeamId Team => team;

        public bool IsEnemyOf(TeamMember other)
        {
            return other != null && team != TeamId.Neutral &&
                   other.team != TeamId.Neutral && team != other.team;
        }
    }
}
