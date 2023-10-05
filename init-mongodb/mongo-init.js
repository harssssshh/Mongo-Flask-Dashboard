print("Started Adding the Users.");
db = db.getSiblingDB("admin");
db.createUser(
  {
    user: "exporter",
    pwd: "password",
    roles: [
        { role: "clusterMonitor", db: "admin" },
        { role: "read", db: "local" }
    ]
  }
);
print("End Adding the User Roles.");
