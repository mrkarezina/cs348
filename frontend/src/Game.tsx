import { Button, Loader, NumberInput, Space, Text } from '@mantine/core';
import { KeyboardEvent, useEffect, useState } from 'react';
import { getGameQuestions, submitScore } from './apiCalls';

export default function Game({ username }: { username: string }) {
    const [questions, setQuestions] = useState<Array<[string, number]>>([]);
    const [score, setScore] = useState(0);
    const [question, setQuestion] = useState(0);
    const [answer, setAnswer] = useState<number | undefined>(0);

    useEffect(() => {
        getGameQuestions().then(questions => setQuestions(questions)).catch(console.error);
    }, []);

    const nextQuestionOrSubmit = () => {
        setScore(oldScore => {
            // mark question as correct if within 5% of the answer
            const correctNess = (answer === undefined ? 0 : answer) / questions[question][1];
            const correct = (correctNess < 1.05 && correctNess > 0.95);
            const newScore = oldScore + (correct ? 1 : 0);
            // submit score after last question is answered
            if (question === questions.length - 1) submitScore(username, newScore);
            setAnswer(0);              // reset input
            setQuestion(question + 1); // go to next question
            return newScore;
        });
    }

    const handleKeyDown = (event: KeyboardEvent) => {
        if (event.key === 'Enter') nextQuestionOrSubmit();
    }

    return <>
        {questions.length === 0 && <Loader />}
        {questions.length === question && <>
            <Text>Your score: {score} / {questions.length}</Text>
            <Text>Answers</Text>
            {questions.map((item, i) => <Text key={i}>Country {item[0]} has area of {item[1]} <span>km<sup>2</sup></span></Text>)}
        </>}
        {questions.length && question < questions.length && <>
            <Text>Q{question + 1} of {questions.length}: Guess the area of {questions[question][0]}?</Text>
            <Space h='md' />
            <NumberInput value={answer} onChange={setAnswer} onKeyDown={handleKeyDown} />
            <Space h='md' />
            <Button onClick={nextQuestionOrSubmit} >{question < questions.length - 1 ? 'Next' : 'See results'}</Button>
        </>}
    </>;
}
