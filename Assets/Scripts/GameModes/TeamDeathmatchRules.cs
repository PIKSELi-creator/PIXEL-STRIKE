using UnityEngine;

namespace PixelStrike.GameModes
{
    public sealed class TeamDeathmatchRules : MonoBehaviour
    {
        [SerializeField, Min(1)] private int scoreLimit = 50;
        public int AlphaScore { get; private set; }
        public int BravoScore { get; private set; }
        public bool MatchEnded { get; private set; }

        public void RegisterElimination(Combat.TeamId scoringTeam)
        {
            if (MatchEnded) return;

            if (scoringTeam == Combat.TeamId.Alpha) AlphaScore++;
            if (scoringTeam == Combat.TeamId.Bravo) BravoScore++;

            if (AlphaScore >= scoreLimit || BravoScore >= scoreLimit)
                MatchEnded = true;
        }

        public void ResetMatch()
        {
            AlphaScore = 0;
            BravoScore = 0;
            MatchEnded = false;
        }
    }
}
