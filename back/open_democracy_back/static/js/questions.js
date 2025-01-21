window.addEventListener('load', function (event) {
    const typeQuestionOptions = document.getElementById("id_type");
    var rulesForResponseChoiceQuestions = document.getElementById("panel-choix_de_reponses_possibles-section")
    var rulesForMultipleChoiceQuestion = document.getElementById("panel-max_multiple_choices-section")
    var rulesForClosedWithScaleQuestion = document.getElementById("panel-categories_pour_une_question_fermee_a_echelle-section")
    var rulesForNumberQuestion = document.getElementById("panel-parametrage_dune_question_de_nombre-section") || document.createElement("div");
    var rulesForPercentageQuestion = document.getElementById("panel-score_associe_aux_reponses_dune_question_de_pourcentage-section") || document.createElement("div");


    function responseRules(questionType) {
        switch (questionType) {
            case "unique_choice":
            case "multiple_choice":
            case "closed_with_scale":
                rulesForResponseChoiceQuestions.style.display = "block";
                rulesForClosedWithScaleQuestion.style.display = "none";
                rulesForMultipleChoiceQuestion.style.display = "none";
                rulesForPercentageQuestion.style.display = "none";
                rulesForNumberQuestion.style.display = "none";
                if (questionType == "multiple_choice") {
                    rulesForMultipleChoiceQuestion.style.display = "block";
                } else if (questionType == "closed_with_scale") {
                    rulesForClosedWithScaleQuestion.style.display = "block";
                }
                break;
            case "boolean":
                rulesForResponseChoiceQuestions.style.display = "none";
                rulesForClosedWithScaleQuestion.style.display = "none";
                rulesForMultipleChoiceQuestion.style.display = "none";
                rulesForPercentageQuestion.style.display = "none";
                rulesForNumberQuestion.style.display = "none";
                break;
            case "percentage":
                rulesForResponseChoiceQuestions.style.display = "none";
                rulesForClosedWithScaleQuestion.style.display = "none";
                rulesForMultipleChoiceQuestion.style.display = "none";
                rulesForPercentageQuestion.style.display = "block";
                // rulesForNumberQuestion.style.display = "none";
                break
            case "number":
                rulesForResponseChoiceQuestions.style.display = "none";
                rulesForClosedWithScaleQuestion.style.display = "none";
                rulesForMultipleChoiceQuestion.style.display = "none";
                rulesForPercentageQuestion.style.display = "none";
                rulesForNumberQuestion.style.display = "block";
                break;
            default:
                rulesForResponseChoiceQuestions.style.display = "none";
                rulesForClosedWithScaleQuestion.style.display = "none";
                rulesForMultipleChoiceQuestion.style.display = "none";
                rulesForPercentageQuestion.style.display = "none";
                rulesForNumberQuestion.style.display = "none";
        }
    }

    responseRules(typeQuestionOptions.value)

    typeQuestionOptions.addEventListener("change", function () {
        responseRules(typeQuestionOptions.value)
    });
});
