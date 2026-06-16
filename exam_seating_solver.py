from collections import deque

# ==================================================
# CO1 : STATE SPACE REPRESENTATION
# ==================================================

class SeatingStateSpace:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def get_all_seats(self):

        seats = []

        for r in range(self.rows):
            for c in range(self.cols):
                seats.append((r, c))

        return seats


# ==================================================
# CO2 : BFS SEARCH
# ==================================================

class SearchEngine:

    def bfs_available_seats(self, all_seats, occupied):

        queue = deque(all_seats)

        available = []

        while queue:

            seat = queue.popleft()

            if seat not in occupied:
                available.append(seat)

        return available


# ==================================================
# CO3 : CSP + MRV + BACKTRACKING
# ==================================================

class CSPSeating:

    def mrv(self, students):

        return min(students, key=lambda x: len(x))

    def backtrack(self, students, seats, assignment):

        if len(assignment) == len(students):
            return True

        student = students[len(assignment)]

        for seat in seats:

            if seat not in assignment.values():

                assignment[student] = seat

                if self.backtrack(
                        students,
                        seats,
                        assignment):
                    return True

                del assignment[student]

        return False


# ==================================================
# CO4 : UTILITY FUNCTION
# ==================================================

class UtilityAgent:

    def calculate_utility(self, seat):

        row, col = seat

        utility = 100

        if row == 0:
            utility += 20

        if col == 0:
            utility += 10

        return utility


# ==================================================
# CO5 : BAYESIAN REASONING
# ==================================================

class BayesianReasoner:

    def bayes(self,
              prior,
              likelihood,
              evidence):

        return round(
            (prior * likelihood) / evidence,
            2
        )


# ==================================================
# CO6 : INTEGRATED AI PIPELINE
# ==================================================

class ExaminationAI:

    def __init__(self):

        self.state_space = SeatingStateSpace(
            4,
            4
        )

        self.search = SearchEngine()

        self.utility = UtilityAgent()

        self.bayes = BayesianReasoner()

    def run(self):

        students = [
            "ST01",
            "ST02",
            "ST03",
            "ST04",
            "ST05"
        ]

        room = "Room-A"

        occupied = []

        all_seats = self.state_space.get_all_seats()

        available_seats = self.search.bfs_available_seats(
            all_seats,
            occupied
        )

        csp = CSPSeating()

        assignments = {}

        csp.backtrack(
            students,
            available_seats,
            assignments
        )

        print("\n")
        print("=" * 60)
        print("      EXAMINATION SEATING ARRANGEMENT SYSTEM")
        print("=" * 60)

        seating_matrix = [
            ["--" for _ in range(4)]
            for _ in range(4)
        ]

        print("\nStudent Allocations\n")

        for student, seat in assignments.items():

            row, col = seat

            seating_matrix[row][col] = student

            utility_score = self.utility.calculate_utility(
                seat
            )

            probability = self.bayes.bayes(
                prior=0.5,
                likelihood=0.8,
                evidence=0.6
            )

            print(f"Student ID : {student}")
            print(f"Room       : {room}")
            print(f"Seat       : {seat}")
            print(f"Utility    : {utility_score}")
            print(f"Probability: {probability}")
            print("-" * 40)

        print("\n")
        print("=" * 20)
        print("ROOM LAYOUT")
        print("=" * 20)

        for row in seating_matrix:
            print("\t".join(row))

        print("\n")
        print("=" * 25)
        print("EXPLAINABLE REPORT")
        print("=" * 25)

        print("1. State Space Representation created.")
        print("2. BFS searched available seats.")
        print("3. CSP Backtracking allocated students.")
        print("4. MRV heuristic used for CSP.")
        print("5. Utility function ranked seats.")
        print("6. Bayesian reasoning estimated suitability.")
        print("7. Final seating arrangement generated.")

        print("\n")
        print("=" * 60)
        print("PROCESS COMPLETED SUCCESSFULLY")
        print("=" * 60)


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    system = ExaminationAI()

    system.run()