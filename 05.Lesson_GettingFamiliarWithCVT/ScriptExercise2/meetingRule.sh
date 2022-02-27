

certoraRun ../04.Lesson_Declarations/Methods_Definitions_Functions/MeetingScheduler/MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:../04.Lesson_Declarations/Methods_Definitions_Functions/MeetingScheduler/meetings.spec \
  --solc solc8.7 \
  --rule startOnTime \
  --msg "$1" \
  --send_only