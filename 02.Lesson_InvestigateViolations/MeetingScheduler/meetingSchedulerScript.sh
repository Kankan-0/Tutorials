
[ $# -eq 3 ] &&
certoraRun "$1":MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--msg "$2" \
--rule "$3"

[ $# -eq 2 ] &&
certoraRun "$1":MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--msg "$2"
