from QuestionSplitter import QuestionSplitter
from Lexer import Lexer
from typing import Optional, Tuple
import json

class Parser:
    def __init__(self):
        pass
    
    def point_remark(self, lexedLine: Lexer) -> dict:
            # Label: <PointRemark>
            # Eval: integer "points"
            savePos = lexedLine.getLoc()
            if (pointsToken := lexedLine.getToken())[0] == "int" and lexedLine.nextToken()[1] == "points":
                PointsRemark = {"Points": pointsToken[1]}
            # Eval: "question" "number" integer "for" integer "points"
            elif lexedLine.setLoc(savePos) and lexedLine.getToken()[1] == "question" and lexedLine.nextToken()[1] == "number" and lexedLine.nextToken()[0] == "int" and lexedLine.nextToken()[1] == "for" and (pointsToken := lexedLine.nextToken())[0] == "int" and lexedLine.nextToken()[1] == "points":
                PointsRemark = {"Points": pointsToken[1]}
            
            return PointsRemark
        
    def question_remark(self, lexedLine: Lexer) -> Optional[dict]:
        QuestionRemark = None

        # Label: <StatementQuestion>
        # Eval: "statement" "and" <PartQuestion>
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if lexedLine.nextToken()[1] == "statement" and lexedLine.nextToken()[1] == "and":
            # Label: <PartQuestion>
            # Eval: integer "part" <STQuestion>
            savePos = lexedLine.getLoc()
            if (partsToken := lexedLine.nextToken())[0] == "int" and lexedLine.nextToken()[1] == "part":
                # Label: <STQuestion>
                # "scripture" "text" <AppQuestion>
                savePos = lexedLine.getLoc()
                if lexedLine.nextToken()[1] == "scripture" and lexedLine.nextToken()[1] == "text":
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        # <QuoteEssenceQuestion>
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Application"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Application", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Application", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Application", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Application", "Quotation"], "Parts": partsToken[1]}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "ScriptureText", "Quotation"], "Parts": partsToken[1]}
                # Eval: <AppQuestion>
                else:
                    lexedLine.setLoc(savePos)
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "Part", "Application"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "Application", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "Application", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "Application", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "Application", "Quotation"], "Parts": partsToken[1]}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "Part"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Part", "Quotation"], "Parts": partsToken[1]}
            # Eval: <STQuestion>
            else:
                lexedLine.setLoc(savePos)
                # Label: <STQuestion>
                # "scripture" "text" <AppQuestion>
                savePos = lexedLine.getLoc()
                if lexedLine.nextToken()[1] == "scripture" and lexedLine.nextToken()[1] == "text":
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        # <QuoteEssenceQuestion>
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Application"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Application", "EssenceCompletion"],"Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Application", "Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Application", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Application", "Quotation"], "Parts": partsToken[1]}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "ScriptureText"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "ScriptureText", "Quotation"], "Parts": partsToken[1] }
                # Eval: <AppQuestion>
                else:
                    lexedLine.setLoc(savePos)
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        # <QuoteEssenceQuestion>
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement", "Application"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Application", "EssenceCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Application", "Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Application", "QuotationCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Application", "Quotation"], "Parts": 0}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Statement"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "EssenceCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "QuotationCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Statement", "Quotation"], "Parts": 0}
        # Eval: <PartQuestion>
        else:
            # Label: <PartQuestion>
            # Eval: integer "part" <STQuestion>
            lexedLine.setLoc(savePos)
            savePos = lexedLine.getLoc()
            if (partsToken := lexedLine.nextToken())[0] == "int" and lexedLine.nextToken()[1] == "part":
                # Label: <STQuestion>
                # "scripture" "text" <AppQuestion>
                savePos = lexedLine.getLoc()
                if lexedLine.nextToken()[1] == "scripture" and lexedLine.nextToken()[1] == "text":
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Application"],"Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Application", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Application", "Quotation"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Application", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Application", "Essence"], "Parts": partsToken[1]}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Part", "ScriptureText"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "ScriptureText", "Quotation"], "Parts": partsToken[1]}
                # Eval: <AppQuestion>
                else:
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    lexedLine.setLoc(savePos)
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Part", "Application"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "Application", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "Application", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "Application", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "Application", "Quotation"], "Parts": partsToken[1]}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Part"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "EssenceCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "Essence"], "Parts": partsToken[1]}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "QuotationCompletion"], "Parts": partsToken[1]}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Part", "Quotation"], "Parts": partsToken[1]}
            # Eval: <STQuestion>
            else:
                lexedLine.setLoc(savePos)
                # Label: <STQuestion>
                # "scripture" "text" <AppQuestion>
                savePos = lexedLine.getLoc()
                if lexedLine.nextToken()[1] == "scripture" and lexedLine.nextToken()[1] == "text":
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        # <QuoteEssenceQuestion>
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["ScriptureText", "Application"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "Application", "EssenceCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "Application", "Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "Application", "QuotationCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "Application", "Quotation"],"Parts": 0}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["ScriptureText"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "EssenceCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "QuotationCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["ScriptureText", "Quotation"], "Parts": 0}
                # Eval: <AppQuestion>
                else:
                    lexedLine.setLoc(savePos)
                    # Label: <AppQuestion>
                    # Eval: "application" <QuoteEssenceQuestion>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "application":
                        # <QuoteEssenceQuestion>
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": ["Application"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Application", "EssenceCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Application", "Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Application", "QuotationCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Application", "Quotation"], "Parts": 0}
                    # Eval: <QuoteEssenceQuestion>
                    else:
                        lexedLine.setLoc(savePos)
                        savePos = lexedLine.getLoc()
                        if lexedLine.nextToken()[1] == "question": # Question
                            QuestionRemark = {"QuestionType": None, "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "essence": # Essence
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["EssenceCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Essence"], "Parts": 0}
                        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "quotation": # Quotation
                            savePos = lexedLine.getLoc()
                            if lexedLine.nextToken()[1] == "completion" and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["QuotationCompletion"], "Parts": 0}
                            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "question":
                                QuestionRemark = {"QuestionType": ["Quotation"], "Parts": 0}
        
        if not QuestionRemark:
            lexedLine.setLoc(retPos)
        return QuestionRemark

    def answer_remark(self, lexedLine: Lexer) -> Optional[dict]:
        AnswerRemark = None
        
        # Label: <AnswerRemark>
        # Eval: <PartAnswer>
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if (partsToken := lexedLine.nextToken())[0] == "int" and lexedLine.nextToken()[1] == "part":
            # Eval: "answer"
            savePos = lexedLine.getLoc()
            if lexedLine.nextToken()[1] == "answer":
                AnswerRemark = {"AnswerType": ["Part"], "Parts": partsToken[1]}
            # Eval: <AnalysisAnswer>
            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "chapter" and lexedLine.nextToken()[1] == "analysis" and lexedLine.nextToken()[1] == "answer":
                AnswerRemark = {"AnswerType": ["Part","Analysis"],"Parts": partsToken[1]}
        # Eval: <AnalysisAnswer>
        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "chapter" and lexedLine.nextToken()[1] == "analysis" and lexedLine.nextToken()[1] == "answer":
            AnswerRemark = {"AnswerType": ["Analysis"], "Parts": 0}
        # Eval: <CompleteAnswer>
        else:
            # Eval: "give" integer "complete" "answers"
            lexedLine.setLoc(savePos)
            savePos = lexedLine.getLoc()
            if lexedLine.nextToken()[1] == "give" and (partsToken := lexedLine.nextToken())[0] == "int" and lexedLine.nextToken()[1] == "complete" and lexedLine.nextToken()[1] == "answers":
                AnswerRemark = {"AnswerType": ["Complete"], "Parts": partsToken[1]}
            # Eval: "give" "a" "complete" "answers"
            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "give" and lexedLine.nextToken()[1] == "a" and lexedLine.nextToken()[1] == "complete" and lexedLine.nextToken()[1] == "answer":
                AnswerRemark = {"AnswerType": ["Complete"], "Parts": 1}
        
        if not AnswerRemark:
            lexedLine.setLoc(retPos)
        return AnswerRemark

    def location_remark(self, lexedLine: Lexer) -> Tuple[Optional[dict], Optional[list]]:
        LocationRemark = (None, None)

        # Label: <LocationRemark>
        # Eval: "from"
        savePos = lexedLine.getLoc()
        if lexedLine.nextToken()[1] == "from":
            # Label: <SepConsRemark>
            # Eval: integer <SepConsWord>
            savePos = lexedLine.getLoc()
            if (verseToken := lexedLine.nextToken())[0] == "int":
                # Label: <SepConsWord>
                # Eval: "consecutive"
                savePos = lexedLine.getLoc()
                if lexedLine.nextToken()[1] == "consecutive":
                    # Eval: "verses" "of" <ScriptureRemark>
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "verses" and lexedLine.nextToken()[1] == "of":
                        LocationRemark = ({"LocationType": ["Consecutive"], "VerseCount": verseToken[1]}, self.scripture_remark(lexedLine))
                    # Eval: "verses"
                    elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "verses":
                        LocationRemark = ({"LocationType": ["Consecutive"], "VerseCount": verseToken[1]}, self.scripture_remark(lexedLine))
                # Eval: "separate"
                elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "separate":
                    # Eval: "verses" "of"
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "verses" and lexedLine.nextToken()[1] == "of":
                        LocationRemark = ({"LocationType": ["Separate"], "VerseCount": verseToken[1]}, self.scripture_remark(lexedLine))
                    # Eval: "verses"
                    elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "verses":
                        LocationRemark = ({"LocationType": ["Separate"], "VerseCount": verseToken[1]}, self.scripture_remark(lexedLine))
            # Eval: <SepConsRemark>
            elif lexedLine.setLoc(savePos):
                # Label: <SepConsWord>
                # Eval: "consecutive"
                savePos = lexedLine.getLoc()
                if lexedLine.nextToken()[1] == "consecutive":
                    # Eval: "verses" "of"
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "verses" and lexedLine.nextToken()[1] == "of":
                        LocationRemark = ({"LocationType": ["Consecutive"], "VerseCount": 0}, self.scripture_remark(lexedLine))
                    # Eval: "verses"
                    elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "verses":
                        LocationRemark = ({"LocationType": ["Consecutive"], "VerseCount": 0}, self.scripture_remark(lexedLine))
                # Eval: "separate"
                elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "separate":
                    # Eval: "verses" "of"
                    savePos = lexedLine.getLoc()
                    if lexedLine.nextToken()[1] == "verses" and lexedLine.nextToken()[1] == "of":
                        LocationRemark = ({"LocationType": ["Separate"], "VerseCount": 0}, self.scripture_remark(lexedLine))
                    # Eval: "verses"
                    elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "verses":
                        LocationRemark = ({"LocationType": ["Separate"], "VerseCount": 0}, self.scripture_remark(lexedLine))
                # Eval: <ScriptureRemark>
                else:
                    lexedLine.setLoc(savePos)
                    LocationRemark = (None, self.scripture_remark(lexedLine))

        return LocationRemark
    
    def scripture_remark(self, lexedLine: Lexer) -> Optional[list]:
        ScriptureRemark = None
        
        # Label: <ScriptureRemark>
        # Eval: "the" "section" "titled" quotedstring
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if lexedLine.nextToken()[1] == "the" and lexedLine.nextToken()[1] == "section" and lexedLine.nextToken()[1] == "titled" and (quote := lexedLine.nextToken())[0] == "quote": 
            ScriptureRemark = [{"Book": None, "Chapters": None, "Section": quote[1]}]
        # Eval: <bookchapterlist>
        elif lexedLine.setLoc(savePos) and (bookchapterlist := self.bookchapterlist(lexedLine)):
            ScriptureRemark = bookchapterlist
        # Eval: <chapters>
        elif lexedLine.setLoc(savePos) and (chapters := self.chapters(lexedLine)):
            ScriptureRemark = [{"Book": None, "Chapters": chapters, "Section": None}]
        # Eval: <booklist>
        elif lexedLine.setLoc(savePos) and (booklist := self.booklist(lexedLine)):
            ScriptureRemark = list()
            for book in booklist:
                ScriptureRemark.append({"Book": book, "Chapters": None, "Section": None})
        
        return ScriptureRemark

    def booklist(self, lexedLine: Lexer) -> Optional[list]:
        finalBooklist = None
        
        # Label: <booklist>
        # Eval: book "and" book
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if (book := lexedLine.nextToken())[0] == "book" and lexedLine.nextToken()[1] == "and" and (book1 := lexedLine.nextToken())[0] == "book":
            finalBooklist = [book[1], book1[1]]
        # Eval: book <booklist>
        elif lexedLine.setLoc(savePos) and (book := lexedLine.nextToken())[0] == "book" and (booklist := self.booklist(lexedLine)):
            finalBooklist = [book[1]] + booklist
        # Eval: book
        elif lexedLine.setLoc(savePos) and (book := lexedLine.nextToken())[0] == "book":
            finalBooklist = [book[1]]
        
        if not finalBooklist:
            lexedLine.setLoc(retPos)
        return finalBooklist
    
    def chapters(self, lexedLine: Lexer) -> Optional[list]:
        finalChapList = None

        # Label: <chapters>
        # Eval: "chapter" integer
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if lexedLine.nextToken()[1] == "chapter" and (chapterToken := lexedLine.nextToken())[0] == "int":
            finalChapList = [chapterToken[1]]
        # Eval: "chapters" <integerlist>
        elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "chapters" and (integerlist := self.integerlist(lexedLine)):
            finalChapList = integerlist
        
        if not finalChapList:
            lexedLine.setLoc(retPos)
        return finalChapList
    
    def integerlist(self, lexedLine: Lexer) -> Optional[list]:
        finalIntList = None

        # Eval: integer "and" integer
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if (int := lexedLine.nextToken())[0] == "int" and lexedLine.nextToken()[1] == "and" and (int1 := lexedLine.nextToken())[0] == "int":
            finalIntList = [int[1], int1[1]]
        # Eval: integer <integerlist>
        elif lexedLine.setLoc(savePos) and (int := lexedLine.nextToken())[0] == "int" and (intlist := self.integerlist(lexedLine)):
            finalIntList = [int[1]] + intlist
        # Eval: integer
        elif lexedLine.setLoc(savePos) and (int := lexedLine.nextToken())[0] == "int":
            finalIntList = [int[1]]
        
        if not finalIntList:
            lexedLine.setLoc(retPos)
        return finalIntList
    
    def bookchapterlist(self, lexedLine: Lexer) -> Optional[list]:
        finalList = None
       
        # Label: <bookchapter>
        # Eval: book <chapters>
        retPos = lexedLine.getLoc()
        savePos = lexedLine.getLoc()
        if (book := lexedLine.nextToken())[0] == "book" and (chapters := self.chapters(lexedLine)):
            # Eval: <bookchapterlist>
            savePos = lexedLine.getLoc()
            if bookchapterlist := self.bookchapterlist(lexedLine):
                finalList = bookchapterlist
            # Eval: "and" <bookchapter>
            elif lexedLine.setLoc(savePos) and lexedLine.nextToken()[1] == "and" and (book1 := lexedLine.nextToken())[0] == "book" and (chapters1 := self.chapters(lexedLine)):
                bookObj = {"Book": book[1], "Chapters": chapters, "Section": None}
                bookObj1 = {"Book": book1[1], "Chapters": chapters1, "Section": None}
                finalList = [bookObj, bookObj1]
            else:
                finalList = [{"Book": book[1], "Chapters": chapters, "Section": None}]
        
        if not finalList:
            lexedLine.setLoc(retPos)
        return finalList
    
    def parse_file(self, inFileName, outFileName):
        split = QuestionSplitter(inFileName)
        
        finalList = list()
        for node in split.splitNodeList:
            lexedLine = Lexer(node[0])
            lexedLine.setLoc(0)

            PointsRemark = self.point_remark(lexedLine)
            QuestionRemark = self.question_remark(lexedLine)
            AnswerRemark = self.answer_remark(lexedLine)
            tmp = self.location_remark(lexedLine)
            LocationRemark = tmp[0]
            ScriptureRemark = tmp[1]
            
            finalNode = {
                "OpeningRemarks": {
                    "PointsRemark": PointsRemark,
                    "QuestionRemark": QuestionRemark,
                    "AnswerRemark": AnswerRemark,
                    "LocationRemark": LocationRemark,
                    "ScriptureRemark": ScriptureRemark
                },
                "QuestionText": node[1],
                "AnswerText": node[2],
                "OriginalText": node[0]+node[1]+node[2]
            }
            finalList.append(finalNode)

        jsonOut = open(outFileName, "w")
        json.dump(finalList, jsonOut, indent=2)
        
