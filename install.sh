cp -R ./runnable ./infrared-controller
cp -R ./infrared-controller /var/opt
rm -rf ./infrared-controller

chown -R pi:pi /var/opt/infrared-controller