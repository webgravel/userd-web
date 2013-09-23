echo "proxy ALL = (ALL) NOPASSWD: /usr/local/bin/gravel-web-gettarget" > /etc/sudoers.d/userd-proxy
chmod 440 /etc/sudoers.d/userd-proxy
export NODE_PATH=/gravel/pkg/bouncy
echo "running node route.js"

quitfun() {
    echo killing node
    kill $pid
    exit 0
}

trap quitfun TERM

while true; do
    node route.js & pid=$!
    wait $pid
    echo "node died unexpectly"
    sleep 3
done
