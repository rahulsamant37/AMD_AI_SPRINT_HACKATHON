@echo off
echo Starting SchedulAI FastAPI Server...
echo.
echo The server will start on http://localhost:5000 (port fixed to match config)
echo API Documentation will be available at http://localhost:5000/docs
echo.
echo To test the /receive endpoint with MetaData:
echo   POST http://localhost:5000/meetings/receive
echo.
echo Authentication Issue Fixed: Now properly loads tokens from Keys directory
echo.
cd /d d:\AMD_AI_SPRINT_HACKATHON
python -m uvicorn app.main:app --reload --port 5000 --host 0.0.0.0
