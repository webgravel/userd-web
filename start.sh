echo "proxy ALL = (ALL) NOPASSWD: /usr/local/bin/gravel-web-gettarget" > /etc/sudoers.d/userd-proxy
chmod 440 /etc/sudoers.d/userd-proxy
export NODE_PATH=/gravel/pkg/bouncy
echo "running node route.js"
exec node route.js
