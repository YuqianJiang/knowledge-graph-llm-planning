## Installation notes:
Install docker and allow it to run without sudo

To visualize graph, run:
```commandline
USER:~/project/llmp/age-viewer$ npm run start
```

- Connect URL: localhost
- Connect Port: 5432
- Database Name: knowledge_base
- User Name: postgres
- Password: password


Installation details:
Setup AGE (https://github.com/apache/age) tricks:
be sure to run https://github.com/apache/age?tab=readme-ov-file#post-installation
```commandline
sudo -u postgres psql -d knowledge_base
CREATE EXTENSION age;
```

Setup the knowledge base:
```commandline
git clone git@github.com:utexas-bwi/knowledge_representation.git
run https://github.com/utexas-bwi/knowledge_representation/blob/master/scripts/configure_postgresql.sh
```

Some specific versions:
- llama_index commit: 502a4d66
- langchain commit: v0.0.272
- PG12/v1.3.0-rc1


## Testing commands:
```commandline
docker run -v .:/root/experiments lapkt/lapkt-public ./siw-then-bfsf --domain /root/experiments/planning/domain.pddl  --problem /root/experiments/experiments/kg/FreezeApple/run2/problem_0.pddl   --output /root/experiments/experiments/kg/FreezeApple/run2/plan_0.pddl
```