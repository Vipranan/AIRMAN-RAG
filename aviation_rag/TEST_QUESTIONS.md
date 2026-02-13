# Aviation RAG System - Test Questions

This document contains 50 test questions organized by category to evaluate the AIRMAN Aviation Document AI Chat system.

## Factual Questions (20)

These questions test the system's ability to retrieve and present factual information from the documents.

1. What does VFR stand for and what does it require?
2. What is the minimum safe altitude over a congested area?
3. Define ATPL and list the privileges it grants.
4. What are the three types of hypoxia?
5. What is the purpose of a pre-flight checklist?
6. What does METAR stand for?
7. What is the standard temperature lapse rate in the troposphere?
8. What is V1 speed?
9. What does the acronym PAVE stand for in risk assessment?
10. What is the maximum demonstrated crosswind component for this aircraft?
11. What are the required documents that must be on board an aircraft?
12. What is the definition of IFR?
13. What is the purpose of the pitot tube?
14. What does QNH represent?
15. What is the standard atmospheric pressure at sea level?
16. What is the function of ailerons?
17. What is the definition of density altitude?
18. What is the purpose of trim tabs?
19. What does CAVOK mean?
20. What are the main types of clouds?

## Applied Questions (20)

These questions test the system's ability to apply knowledge to practical scenarios.

21. If the outside air temperature is higher than standard, how does it affect density altitude?
22. During a pre-flight inspection, you notice a small dent on the leading edge of the wing. What should you do?
23. You are planning a VFR flight and the forecast shows visibility of 3 miles. Can you legally depart?
24. What actions should a pilot take if carburetor icing is suspected?
25. How do you calculate weight and balance for a flight with two passengers and baggage?
26. What is the correct procedure for entering a controlled airspace?
27. If you encounter windshear on final approach, what should you do?
28. How should a pilot adjust the altimeter when transitioning from one pressure area to another?
29. What is the procedure for a short field takeoff?
30. If the engine fails immediately after takeoff, what are the first actions?
31. How do you determine if an aircraft is within CG limits before flight?
32. What should you do if you inadvertently enter IMC while flying VFR?
33. How does increasing altitude affect engine performance in a normally aspirated engine?
34. What is the correct radio phraseology to request taxi clearance?
35. If you notice the oil pressure gauge reading zero during cruise flight, what immediate actions should you take?
36. How do you calculate the required runway length for takeoff at a high-altitude airport?
37. What is the procedure for recovering from a spin?
38. How should a pilot respond to a TCAS RA (Resolution Advisory)?
39. What factors should be considered when planning a flight over mountainous terrain?
40. If you experience an electrical fire in flight, what is the immediate action?

## Reasoning Questions (10)

These questions test the system's ability to explain concepts and reasoning.

41. Why is it dangerous to fly through a thunderstorm, and what alternatives should a pilot consider?
42. Explain the relationship between angle of attack, lift, and stall.
43. Why must a pilot consider both pressure altitude and temperature when calculating density altitude?
44. What are the risks of spatial disorientation, and how can a pilot prevent it?
45. Why is it important to lean the mixture at high altitude, and what happens if you don't?
46. Explain the decision-making process for a go-around versus continuing an unstable approach.
47. Why does an aircraft require more runway for takeoff on a hot day compared to a cold day?
48. What are the aerodynamic effects of ice accumulation on the wings?
49. Why is crew resource management (CRM) essential in multi-crew operations?
50. Explain why a pilot should not attempt to stretch a glide to reach a runway during an engine failure.

---

## Testing Instructions

### Manual Testing
1. Start the AIRMAN web interface at http://localhost:8000
2. Ask each question one by one
3. Evaluate the responses for:
   - Accuracy (does it answer the question correctly?)
   - Completeness (is the answer thorough?)
   - Citations (are proper sources provided?)
   - Faithfulness (does the answer match the retrieved context?)

### Automated Testing
Run the evaluation script:
```bash
python evaluate.py
```

This will test all questions from `questions.json` and generate metrics including:
- Retrieval hit rate
- Average faithfulness score
- Hallucination rate
- No-answer rate
- Average latency

### Expected Behavior

**Good Responses:**
- Provides accurate information from the documents
- Cites specific sources (document name and page number)
- High faithfulness score (>0.70)
- Clear and concise answers

**Acceptable Responses:**
- Returns "This information is not available in the provided document(s)" when the answer isn't in the documents
- Better to say "not available" than to hallucinate

**Poor Responses:**
- Makes up information not in the documents (hallucination)
- Low faithfulness score (<0.70)
- Provides irrelevant or incorrect information

---

## Sample Expected Answers

### Question: What are the main types of clouds?

**Expected Answer:**
The three basic forms of cloud are:
1. Stratiform (layered type of cloud with little vertical extent)
2. Cumuliform (heaped cloud with marked vertical extent)
3. Cirriform (cloud which is fibrous, wispy or hair-like in appearance)

**Source:** Meteorology full book.pdf

### Question: What is the purpose of mass and balance calculations?

**Expected Answer:**
The purpose of mass and balance calculations is to determine the Basic Empty Mass (BEM) and Centre of Gravity position of an aircraft. This information is necessary for safe operation, as it affects the loading and stability of the aircraft.

**Source:** 6-mass-and-balance-and-performance-2014.pdf

### Question: What does VFR stand for?

**Expected Answer:**
If the documents don't explicitly define VFR, the system should return:
"This information is not available in the provided document(s)."

This is correct behavior - better to admit lack of information than to hallucinate.

---

## Performance Benchmarks

Based on the evaluation of 50 questions, target metrics:

| Metric | Target | Acceptable | Poor |
|--------|--------|------------|------|
| Retrieval Hit Rate | >70% | 50-70% | <50% |
| Avg Faithfulness | >0.75 | 0.65-0.75 | <0.65 |
| Hallucination Rate | <5% | 5-10% | >10% |
| No-Answer Rate | 10-30% | 30-50% | >50% |
| Avg Latency | <5s | 5-10s | >10s |

**Note:** A high no-answer rate isn't necessarily bad - it means the system is being conservative and not making up information when it doesn't have sufficient context.

---

## Additional Test Scenarios

### Edge Cases
1. **Ambiguous questions:** "What is the speed?" (which speed?)
2. **Out-of-scope questions:** "What's the weather today?" (not in documents)
3. **Multi-part questions:** "What is VFR and IFR and how do they differ?"
4. **Very specific questions:** "What is the fuel capacity of a Cessna 172?"
5. **Contradictory information:** Test if documents have conflicting info

### Stress Testing
1. Very long questions (>200 words)
2. Questions with special characters
3. Questions in different languages (if supported)
4. Rapid-fire questions (test latency under load)
5. Concurrent users (if testing multi-user scenarios)

---

## Troubleshooting

### If many questions return "not available":
- Check if documents were properly ingested
- Verify FAISS index contains all chunks
- Review similarity threshold (currently 0.35)
- Check if faithfulness threshold is too strict (currently 0.70)

### If responses are slow:
- Verify GPU is being used for embeddings
- Check Ollama is running with GPU support
- Monitor system resources (RAM, VRAM)
- Consider reducing batch size or top_k

### If hallucinations occur:
- Increase faithfulness threshold
- Review prompt template in rag.py
- Check if LLM temperature is too high (should be 0.0)
- Verify retrieval is finding relevant chunks

---

## Continuous Improvement

After testing, consider:
1. Adding more documents to improve coverage
2. Fine-tuning chunk size and overlap
3. Adjusting similarity and faithfulness thresholds
4. Implementing query expansion for better retrieval
5. Adding conversation history for multi-turn dialogues
6. Creating a feedback mechanism for users to rate answers

---

**Last Updated:** February 12, 2026
**System Version:** AIRMAN v1.0.0
**Document Count:** 7 PDFs (3,983 chunks)
