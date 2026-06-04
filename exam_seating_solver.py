"""
Title: Automated Examination Seating Arrangement Engine
Description: A unified, single-file AI pipeline that solves seating layout optimizations
             and provides trace-proof explanations when encountering over-constrained failure states.
"""

import copy


# =====================================================================
# PROBLEM FORMULATION & STATE SPACE REPRESENTATION
# =====================================================================
class SeatingStateSpace:
    """
    Handles the spatial coordinates and room geometry definitions.
    """

    def __init__(self, rooms_map):
        self.rooms_map = rooms_map
        self.all_seats = []
        self._build_grid_coordinates()

    def _build_grid_coordinates(self):
        """Generates coordinate lists for all rooms."""
        for room_name, (total_rows, total_cols) in self.rooms_map.items():
            for row_idx in range(total_rows):
                for col_idx in range(total_cols):
                    self.all_seats.append((room_name, row_idx, col_idx))

    @staticmethod
    def is_physically_adjacent(seat1, seat2):
        """Checks if two seats are adjacent vertically, horizontally, or diagonally."""
        room1, r1, c1 = seat1
        room2, r2, c2 = seat2
        if room1 != room2:
            return False
        return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1


# =====================================================================
# CONSTRAINT SATISFACTION PROBLEM (CSP) ENGINE
# =====================================================================
class ExamSeatingCSPEngine:
    def __init__(self, state_space, students_list, special_requirements, exam_papers_map):
        self.state_space = state_space
        self.students = students_list
        self.special_reqs = special_requirements
        self.exam_papers = exam_papers_map

        # Diagnostic Store: Tracks exactly why a seat is restricted for any student
        self.failure_diagnostics = {student: {} for student in students_list}

    def extract_valid_seats_for_student(self, student, current_assignments):
        """Applies rigorous constraint checking to return legal seats for a student."""
        legal_seats = []
        target_exam = self.exam_papers[student]
        reqs = self.special_reqs.get(student, [])

        for seat in self.state_space.all_seats:
            if seat in current_assignments.values():
                continue

                # Constraint 1: Special Accessibility Tag Check (Must sit in Row 0)
            if 'accessible' in reqs and seat[1] != 0:
                self.failure_diagnostics[student][seat] = "Requires accessible accommodation (Row 0 desk)"
                continue

            # Constraint 2: Academic Cheating Prevention / Adjacency Check
            has_conflict = False
            for active_student, active_seat in current_assignments.items():
                if self.exam_papers[active_student] == target_exam:
                    if self.state_space.is_physically_adjacent(seat, active_seat):
                        self.failure_diagnostics[student][
                            seat] = f"Adjacency conflict with {active_student} writing {target_exam}"
                        has_conflict = True
                        break

            if not has_conflict:
                legal_seats.append(seat)

        return legal_seats

    def apply_mrv_heuristic(self, unassigned_list, current_assignments):
        """Heuristic Selector: Evaluates remaining legal seats option counts."""
        min_options_found = float('inf')
        selected_student = unassigned_list[0]

        for student in unassigned_list:
            available_count = len(self.extract_valid_seats_for_student(student, current_assignments))
            if available_count < min_options_found:
                min_options_found = available_count
                selected_student = student

        return selected_student, min_options_found

    def execute_seating_pipeline(self):
        """Initializes and runs the core Backtracking Search layout processing."""
        assignments_map = {}
        unassigned_students = list(self.students)

        search_success = self._backtrack_recursive(unassigned_students, assignments_map)

        if search_success:
            return assignments_map, None
        else:
            failure_report = self.generate_explainable_proof_of_failure(assignments_map)
            return None, failure_report

    def _backtrack_recursive(self, unassigned_list, current_assignments):
        if not unassigned_list:
            return True

        target_student, dynamic_domain_size = self.apply_mrv_heuristic(unassigned_list, current_assignments)

        if dynamic_domain_size == 0:
            return False

        valid_candidate_seats = self.extract_valid_seats_for_student(target_student, current_assignments)
        unassigned_list.remove(target_student)

        for seat in valid_candidate_seats:
            current_assignments[target_student] = seat

            if self._backtrack_recursive(unassigned_list, current_assignments):
                return True

            del current_assignments[target_student]

        unassigned_list.append(target_student)
        return False

    # =====================================================================
    # DIAGNOSTIC REPORT GENERATOR
    # =====================================================================
    def generate_explainable_proof_of_failure(self, partial_assignments):
        """Constructs human-readable structural failure proofs based on diagnostic data."""
        lines = [
            "===========================================================",
            "             SYSTEM DIAGNOSTIC REPORT: SEATING FAILURE     ",
            "===========================================================",
            f"STATUS: Process Halted. Over-constrained system parameters detected.",
            f"Successfully assigned: {len(partial_assignments)} out of {len(self.students)} students.",
            "\nCRITICAL BOTTLENECK ANALYSIS FOR UNPLACED STUDENTS:"
        ]

        leftover_students = [s for s in self.students if s not in partial_assignments]

        for student in leftover_students:
            lines.append(f"\nStudent ID: {student}")
            lines.append(f" ↳ Registered Exam Paper: {self.exam_papers[student]}")
            lines.append(f" ↳ Physical Request Tags: {self.special_reqs.get(student, [])}")
            lines.append(" ↳ Structural Constraint Isolation Map:")

            reason_counts = {}
            for seat, constraint_trigger in self.failure_diagnostics[student].items():
                reason_counts[constraint_trigger] = reason_counts.get(constraint_trigger, 0) + 1

            for trigger, count in reason_counts.items():
                lines.append(f"    - Blocked from {count} physical desks due to: {trigger}")

        return "\n".join(lines)


# =====================================================================
# EXECUTION WORKFLOW PIPELINE (MAIN TEST SUITE)
# =====================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("SYSTEM INITIATED: PROCESSING TEST CASE RUNS")
    print("=" * 65)

    # --- SCENARIO A: SUCCESSFUL BALANCED SEATING ARRANGEMENT ---
    print("\n[RUN 1: PROCESSING COMPLIANT ENVIRONMENT]")

    room_config_A = {'Main_Hall': (3, 3)}
    students_A = ['ST_01', 'ST_02', 'ST_03', 'ST_04']
    exams_A = {'ST_01': 'DATA_STRUCTURES', 'ST_02': 'ALGORITHMS', 'ST_03': 'DATA_STRUCTURES', 'ST_04': 'ALGORITHMS'}
    reqs_A = {'ST_01': ['accessible']}

    space_A = SeatingStateSpace(room_config_A)
    solver_A = ExamSeatingCSPEngine(space_A, students_A, reqs_A, exams_A)
    success_layout, _ = solver_A.execute_seating_pipeline()

    if success_layout:
        print("✔ Seating Layout Configured Successfully:")
        for stu, (room, r, c) in sorted(success_layout.items()):
            print(f"  Student {stu} ({exams_A[stu]}) ➔ Room: {room}, Desk: [Row {r}, Col {c}]")

    # --- SCENARIO B: OVER-CONSTRAINED FAILURE SCENARIO ---
    print("\n[RUN 2: PROCESSING OVER-CONSTRAINED ENVIRONMENT]")

    room_config_B = {'Mini_Exam_Room': (2, 2)}
    students_B = ['ST_91', 'ST_92', 'ST_93', 'ST_94']
    exams_B = {'ST_91': 'AI_SYSTEMS', 'ST_92': 'AI_SYSTEMS', 'ST_93': 'AI_SYSTEMS', 'ST_94': 'AI_SYSTEMS'}
    reqs_B = {}

    space_B = SeatingStateSpace(room_config_B)
    solver_B = ExamSeatingCSPEngine(space_B, students_B, reqs_B, exams_B)
    _, explainable_error_log = solver_B.execute_seating_pipeline()

    if explainable_error_log:
        print("❌ System Correctly Detected Over-Constrained Constraints.\n")
        print(explainable_error_log)

    print("\n" + "=" * 65)
    print("SYSTEM PROCESSING TERMINATED SUCCESSFULLY")
    print("=" * 65)