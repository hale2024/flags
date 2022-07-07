# the challenge needs to be launched through another shell script,
# this one just interacts with the connection
exec 9</dev/tcp/localhost/1319;

while read -r line <&9; do
    echo "$line";
    read sol;
    [[ ! -z $sol ]] && echo $sol >&9;
done
