def calculate_score(test: dict, answers: list) -> dict:
    total_score = 0
    obtained_score = 0
    detailed_results = []

    for question_obj in test["questions"]:
        question_text = question_obj["question"]
        correct_answer = question_obj["correct_answer"]
        question_score = question_obj["score"]

        total_score += question_score

        user_answer_obj = next((a for a in answers if a.question == question_text), None)

        if user_answer_obj:
            selected_answer = user_answer_obj.selected_answer

            # ✅ Smart compare:
            is_correct = (
                selected_answer.strip().lower() == correct_answer.strip().lower()  # ✅ match texte exact
                or selected_answer.strip().upper().startswith(correct_answer.strip().upper() + ")")  # ✅ match lettre style "B) ... "
            )

            if is_correct:
                obtained_score += question_score
        else:
            selected_answer = None
            is_correct = False

        detailed_results.append({
            "question": question_text,
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "score_awarded": question_score if is_correct else 0
        })

    score_percent = round((obtained_score / total_score) * 100, 2)
    pass_status = "Passed" if score_percent >= test["minimum_score_to_pass"] else "Failed"

    return {
        "total_score": obtained_score,
        "score_percent": score_percent,
        "pass_score_required": test["minimum_score_to_pass"],
        "status": pass_status,
        "details": detailed_results
    }
