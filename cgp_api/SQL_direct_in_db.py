
## Create table for initial setup
CreateTableSQL = """CREATE TABLE comms (
	id serial4 NOT NULL,
	"node" varchar NOT NULL,
	"message" varchar NOT NULL,
	"action" varchar NOT NULL
)"""
# partition by list ("node");"""
