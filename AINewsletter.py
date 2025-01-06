#!/usr/bin/env python
import sys
from src.AINewsletterAgent.crew import AINewsLetterAgents
from datetime import datetime


def run():
    inputs={
        'current_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # current timestamp for the test
    }
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    return AINewsLetterAgents().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()