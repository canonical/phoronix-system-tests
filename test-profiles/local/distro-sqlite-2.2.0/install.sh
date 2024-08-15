#!/bin/sh
tar -zxvf pts-sqlite-tests-1.tar.gz
tar -zxvf sqlite-autoconf-3410200.tar.gz
mkdir sqlite_/
echo "#!/bin/bash
thread_num=\$1
if ! [[ \"\$thread_num\" =~ ^[0-9]+$ ]]
    then
        thread_num=1
fi
cat sqlite-2500-insertions.txt > sqlite-insertions.txt
do_test() {
    DB=benchmark-\$1.db
    /usr/bin/sqlite3 \$DB  \"CREATE TABLE pts1 ('I' SMALLINT NOT NULL, 'DT' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 'F1' VARCHAR(4) NOT NULL, 'F2' VARCHAR(16) NOT NULL);\"
    cat sqlite-insertions.txt | /usr/bin/sqlite3 \$DB
    cat sqlite-insertions.txt | /usr/bin/sqlite3 \$DB
    cat sqlite-insertions.txt | /usr/bin/sqlite3 \$DB
}
pids=\"\"
for i in \$(seq 1 \$thread_num)
do
    do_test \$i &
    pids=\"\$pids \$!\"
done
wait \$pids" > sqlite-benchmark
chmod +x sqlite-benchmark
