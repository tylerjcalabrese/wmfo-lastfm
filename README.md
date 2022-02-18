# WMFO last.fm Scrobbler
By Tyler Calabrese
February 2022

Scrobbles the tracks currently listed on the WMFO homepage to the given
last.fm account.

User will need their own last.fm API account (key and secret). Please
create a .env file with 'API_KEY', 'API_SECRET', 'USERNAME', and 
'HASHED_PASS' before running the application.

To scrobble a previous show's playlist, supply the optional
--from-schedule argument with the show's name, and if it was on a
different day of the week, the --date argument with the date.
Does not support scrobbling shows from the previous week, i.e. the
installment of the show you want to scrobble should appear right away
when you open www.wmfo.org/schedule.

