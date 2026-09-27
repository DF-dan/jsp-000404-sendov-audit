import Mathlib.Tactic

/-!
A branch-specific exact certificate for the 17-point direction model.

The ten order assumptions below occur in one rational model at `t = 9/2`.
They imply `9/2 ≤ t` by a ten-inequality telescoping cycle.  This theorem
does not exclude other branches and is not a proof of JSP-000404.
-/

namespace JSP404.Branch17Certificate

def Triangle (t a b c : ℝ) : Prop :=
  (a ≤ b ∧ b ≤ c ∧ 1 ≤ c - a ∧ b - a ≤ t - 1 ∧ c - b ≤ t - 1) ∨
  (c ≤ b ∧ b ≤ a ∧ 1 ≤ a - c ∧ a - b ≤ t - 1 ∧ b - c ≤ t - 1)

structure Model (t : ℝ) where
  theta : Fin 17 → Fin 17 → ℝ
  triangle : ∀ i j k : Fin 17, i < j → j < k →
    Triangle t (theta i j) (theta i k) (theta j k)

private theorem forward_of_order {t a b c : ℝ} (h : Triangle t a b c)
    (hab : a ≤ b) (hbc : b ≤ c) :
    a ≤ b ∧ b ≤ c ∧ 1 ≤ c - a ∧ b - a ≤ t - 1 ∧ c - b ≤ t - 1 := by
  rcases h with h | ⟨hcb, hba, hspan, _, _⟩
  · exact h
  · exfalso
    linarith

private theorem reverse_of_order {t a b c : ℝ} (h : Triangle t a b c)
    (hcb : c ≤ b) (hba : b ≤ a) :
    c ≤ b ∧ b ≤ a ∧ 1 ≤ a - c ∧ a - b ≤ t - 1 ∧ b - c ≤ t - 1 := by
  rcases h with ⟨hab, hbc, hspan, _, _⟩ | h
  · exfalso
    linarith
  · exact h

/-- These ten order decisions form a local obstruction to `t < 9/2`
for one combinatorial branch.  No range assumptions are needed. -/
theorem branch_forces_half_step {t : ℝ} (m : Model t)
    (h012 : m.theta 1 2 ≤ m.theta 0 2 ∧ m.theta 0 2 ≤ m.theta 0 1)
    (h016 : m.theta 1 6 ≤ m.theta 0 6 ∧ m.theta 0 6 ≤ m.theta 0 1)
    (h0214 : m.theta 0 2 ≤ m.theta 0 14 ∧ m.theta 0 14 ≤ m.theta 2 14)
    (h168 : m.theta 6 8 ≤ m.theta 1 8 ∧ m.theta 1 8 ≤ m.theta 1 6)
    (h21416 : m.theta 2 14 ≤ m.theta 2 16 ∧ m.theta 2 16 ≤ m.theta 14 16)
    (h568 : m.theta 5 6 ≤ m.theta 5 8 ∧ m.theta 5 8 ≤ m.theta 6 8)
    (h5614 : m.theta 6 14 ≤ m.theta 5 14 ∧ m.theta 5 14 ≤ m.theta 5 6)
    (h61114 : m.theta 11 14 ≤ m.theta 6 14 ∧ m.theta 6 14 ≤ m.theta 6 11)
    (h111214 : m.theta 11 12 ≤ m.theta 11 14 ∧ m.theta 11 14 ≤ m.theta 12 14)
    (h121416 : m.theta 14 16 ≤ m.theta 12 16 ∧ m.theta 12 16 ≤ m.theta 12 14) :
    (9 : ℝ) / 2 ≤ t := by
  obtain ⟨_, _, _, hA, _⟩ :=
    reverse_of_order (m.triangle 0 1 2 (by decide) (by decide)) h012.1 h012.2
  obtain ⟨_, _, hB, _, _⟩ :=
    reverse_of_order (m.triangle 0 1 6 (by decide) (by decide)) h016.1 h016.2
  obtain ⟨_, _, hC, _, _⟩ :=
    forward_of_order (m.triangle 0 2 14 (by decide) (by decide)) h0214.1 h0214.2
  obtain ⟨_, _, hD, _, _⟩ :=
    reverse_of_order (m.triangle 1 6 8 (by decide) (by decide)) h168.1 h168.2
  obtain ⟨_, _, hE, _, _⟩ :=
    forward_of_order (m.triangle 2 14 16 (by decide) (by decide)) h21416.1 h21416.2
  obtain ⟨_, _, hF, _, _⟩ :=
    forward_of_order (m.triangle 5 6 8 (by decide) (by decide)) h568.1 h568.2
  obtain ⟨_, _, hG, _, _⟩ :=
    reverse_of_order (m.triangle 5 6 14 (by decide) (by decide)) h5614.1 h5614.2
  obtain ⟨hH, _, _, _, _⟩ :=
    reverse_of_order (m.triangle 6 11 14 (by decide) (by decide)) h61114.1 h61114.2
  obtain ⟨_, _, _, _, hI⟩ :=
    forward_of_order (m.triangle 11 12 14 (by decide) (by decide)) h111214.1 h111214.2
  obtain ⟨_, _, hJ, _, _⟩ :=
    reverse_of_order (m.triangle 12 14 16 (by decide) (by decide)) h121416.1 h121416.2
  linarith

#print axioms branch_forces_half_step

end JSP404.Branch17Certificate
