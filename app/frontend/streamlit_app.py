# app/frontend/streamlit_app.py

import streamlit as st
import pandas as pd
import requests
import pdfplumber
import altair as alt
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API URL (can be configured via environment variable)
BACKEND_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 30

# Page configuration
st.set_page_config(
    page_title="SkillBridge-AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🧠 SkillBridge-AI")
st.markdown(
    "Analyze skill gaps, generate learning paths, and get AI-guided explanations for career growth."
)

# ==============================
# Utility Functions
# ==============================


def check_backend_health() -> bool:
    """Check if backend API is accessible."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def parse_resume_text(resume_text: str) -> List[str]:
    """
    Extract skills from resume text with filtering for relevant technical and professional skills.
    Filters out common words and generic terms.
    """
    import re

    # Common stopwords and irrelevant terms to exclude
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'include', 'including',
        'such', 'as', 'from', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 's', 't', 'can', 'just', 'don', 'now', 'also', 'year', 'years',
        'experience', 'job', 'position', 'role', 'work', 'responsible', 'involved', 'team', 'member',
        'company', 'organization', 'department', 'etc', 'time', 'day', 'month', 'week', 'project',
        'projects', 'develop', 'developed', 'develop', 'support', 'manage', 'managed', 'implement',
        'implemented', 'design', 'designed', 'create', 'created', 'build', 'built', 'maintain',
        'maintained', 'improve', 'improved', 'enhance', 'enhanced', 'performance', 'quality',
        'success', 'successful', 'strong', 'excellent', 'good', 'able', 'required', 'requirement',
        'requirements', 'knowledge', 'experience', 'background', 'skills', 'skill', 'proficiency',
        'proficient', 'familiar', 'familiarity', 'ability', 'understand', 'understanding'
    }

    # Technical skill patterns (keywords that likely indicate skills)
    # Comprehensive list covering 1000+ keywords across all engineering disciplines
    technical_keywords = {
        # Programming Languages (50+)
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby', 'php', 'go', 'golang',
        'rust', 'swift', 'kotlin', 'scala', 'r', 'julia', 'matlab', 'perl', 'groovy', 'clojure',
        'elixir', 'erlang', 'haskell', 'lisp', 'ocaml', 'f#', 'lua', 'dart', 'objective-c', 'vb.net',
        'visual basic', 'cobol', 'fortran', 'ada', 'pascal', 'scheme', 'prolog', 'asm', 'assembly',
        'bash', 'shell', 'powershell', 'perl6', 'raku', 'crystal', 'nim', 'd', 'zig', 'v',
        'move', 'solidity', 'vyper', 'circom', 'graphql', 'sparql', 'datalog', 'agda', 'idris',

        # Web Technologies (80+)
        'html', 'css', 'scss', 'sass', 'less', 'tailwind', 'bootstrap', 'foundation', 'materialize',
        'react', 'reactjs', 'vue', 'vuejs', 'angular', 'angularjs', 'next', 'nextjs', 'nuxt', 'nuxtjs',
        'svelte', 'ember', 'backbone', 'knockout', 'dojo', 'polymer', 'web components', 'axios',
        'fetch', 'jquery', 'lodash', 'underscore', 'ramda', 'immer', 'redux', 'mobx', 'zustand',
        'recoil', 'jotai', 'valtio', 'xstate', 'storybook', 'webpack', 'vite', 'rollup', 'parcel',
        'esbuild', 'gulp', 'grunt', 'broccoli', 'browserify', 'snowpack', 'turbopack', 'babel',
        'prettier', 'eslint', 'typescript', 'flow', 'jest', 'vitest', 'mocha', 'jasmine', 'karma',
        'cypress', 'playwright', 'puppeteer', 'nightwatch', 'webdriver', 'protractor',

        # Backend Frameworks (80+)
        'django', 'flask', 'fastapi', 'tornado', 'pyramid', 'bottle', 'cherrypy', 'web2py',
        'spring', 'spring boot', 'spring mvc', 'spring security', 'grails', 'play', 'akka',
        'laravel', 'symfony', 'yii', 'cakephp', 'zend', 'slim', 'fat-free', 'code igniter',
        'rails', 'rails framework', 'sinatra', 'padrino', 'hanami', 'camping', 'cuba', 'trailblazer',
        'express', 'koa', 'hapi', 'fastify', 'restify', 'strapi', 'meteor', 'sails', 'adonis',
        'nest', 'nestjs', 'feathers', 'loopback', 'graphql server', 'apollo', 'hasura', 'postgraphile',
        'gin', 'echo', 'beego', 'revel', 'buffalo', 'iris', 'fiber', 'chi', 'gorilla', 'martini',
        'vapor', 'perfect', 'kitura', 'ktor', 'micronaut', 'helidon', 'dropwizard', 'lagom',
        'axon', 'quarkus', 'vertx', 'payara', 'glassfish', 'tomcat', 'jetty', 'undertow',

        # Databases & Data (120+)
        'sql', 'nosql', 'postgresql', 'postgres', 'mysql', 'mariadb', 'oracle', 'mssql', 'tsql',
        'sqlite', 'h2', 'db2', 'firebird', 'sybase', 'informix', 'teradata', 'vertica', 'snowflake',
        'redshift', 'bigquery', 'clickhouse', 'druid', 'presto', 'impala', 'hive', 'spark sql',
        'mongodb', 'dynamodb', 'cosmosdb', 'couchdb', 'rethinkdb', 'cassandra', 'hbase', 'bigtable',
        'scylla', 'elasticsearch', 'solr', 'meilisearch', 'typesense', 'algolia', 'sphinx', 'lucene',
        'redis', 'memcached', 'hazelcast', 'ehcache', 'caffeine', 'ignite', 'aerospike', 'tarantool',
        'rockdb', 'leveldb', 'lmdb', 'berkeleydb', 'neo4j', 'arangodb', 'dgraph', 'orientdb',
        'tigergraph', 'neptune', 'tinkerpop', 'sparql', 'virtuoso', 'stardog', 'allegrograph',
        'firebase', 'realtime database', 'firestore', 'supabase', 'realm', 'objectbox', 'couchbase',
        'etcd', 'consul', 'zookeeper', 'kafka', 'rabbit', 'activemq', 'qpid', 'nats', 'zeromq',
        'grpc', 'thrift', 'avro', 'protobuf', 'parquet', 'orc', 'msgpack', 'flatbuffers',
        'arrow', 'polars', 'dask', 'ray', 'rapids', 'vaex', 'modin', 'koalas',

        # Data Science & ML (100+)
        'tensorflow', 'pytorch', 'keras', 'sklearn', 'scikit-learn', 'xgboost', 'lightgbm', 'catboost',
        'ml', 'ai', 'nlp', 'llm', 'cv', 'computer vision', 'deep learning', 'machine learning',
        'numpy', 'pandas', 'scipy', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'altair', 'holoviews',
        'statsmodels', 'patsy', 'sympy', 'networkx', 'igraph', 'graph-tool', 'snap', 'deepchem',
        'jax', 'flax', 'trax', 'dm-tree', 'jax numpy', 'equinox', 'optax', 'dm-haiku', 'dm-acme',
        'hugging face', 'transformers', 'diffusers', 'datasets', 'accelerate', 'peft', 'bitsandbytes',
        'langchain', 'llama index', 'chromadb', 'pinecone', 'weaviate', 'milvus', 'qdrant', 'vespa',
        'openai', 'anthropic', 'cohere', 'replicate', 'together', 'baseten', 'anyscale', 'ray serve',
        'mlflow', 'kubeflow', 'airflow', 'prefect', 'dbt', 'great expectations', 'super ml', 'h2o',
        'dataiku', 'sagemaker', 'vertex ai', 'azure ml', 'databricks', 'domino', 'cnvrg', 'union ai',
        'reinforcement learning', 'rl', 'gym', 'stable baselines', 'ray rllib', 'rllib', 'openai gym',
        'regression', 'classification', 'clustering', 'anomaly detection', 'dimensionality reduction',
        'feature engineering', 'feature extraction', 'data preprocessing', 'data cleaning', 'eda',
        'cross validation', 'hyperparameter tuning', 'grid search', 'random search', 'bayesian optimization',
        'ensemble methods', 'bagging', 'boosting', 'stacking', 'blending', 'voting', 'mixture of experts',
        'attention mechanism', 'transformer', 'bert', 'gpt', 'gpt2', 'gpt3', 'gpt4', 'claude', 'gemini',
        'lstm', 'gru', 'rnn', 'cnn', 'autoencoder', 'vae', 'gan', 'diffusion', 'score based',
        'rnvp', 'glow', 'flow matching', 'ode solver', 'neural ode', 'implicit models', 'energy based',
        'gradient boosting', 'random forest', 'decision tree', 'svm', 'naive bayes', 'knn', 'kmeans',
        'hierarchical clustering', 'dbscan', 'hdbscan', 'spectral clustering', 'gaussian mixture',
        'pca', 'tsne', 'umap', 'manifold learning', 'autoencoders', 'word2vec', 'doc2vec', 'fasttext',
        'glove', 'elmo', 'contextual embeddings', 'knowledge graph embedding', 'graph neural networks',
        'graph convolution', 'message passing', 'graph attention', 'graphsage', 'heterogeneous graphs',

        # Cloud Platforms (80+)
        'aws', 'amazon web services', 'ec2', 'ecs', 'eks', 'elastic beanstalk', 's3', 's3 bucket',
        'lambda', 'rds', 'dynamodb', 'elasticache', 'elb', 'alb', 'nlb', 'route53', 'cloudfront',
        'cloudformation', 'cloudtrail', 'cloudwatch', 'sns', 'sqs', 'kinesis', 'firehose', 'msk',
        'emr', 'athena', 'glue', 'step functions', 'sagemaker', 'rekognition', 'comprehend', 'lex',
        'textract', 'forecast', 'lookout', 'lookoutforvision', 'monitron', 'personalize', 'forecast',
        'azure', 'microsoft azure', 'virtual machines', 'app service', 'container instances', 'aks',
        'cosmos db', 'sql database', 'storage account', 'blob storage', 'queue storage', 'table storage',
        'event hub', 'service bus', 'stream analytics', 'data factory', 'data lake', 'synapse', 'fabric',
        'machine learning studio', 'ml operations', 'mlops', 'cognitive services', 'computer vision',
        'speech services', 'language services', 'translator', 'bot service', 'search service', 'cdn',
        'gcp', 'google cloud', 'google cloud platform', 'compute engine', 'app engine', 'cloud run',
        'cloud functions', 'gke', 'cloud storage', 'cloud sql', 'firestore', 'datastore', 'cloud bigtable',
        'cloud dataflow', 'cloud dataproc', 'bigquery', 'cloud pub/sub', 'cloud tasks', 'cloud scheduler',
        'cloud memorystore', 'cloud cdn', 'cloud load balancing', 'cloud armor', 'cloud vpn', 'cloud vpn',
        'vertex ai', 'ai platform', 'automl', 'cloud vision', 'cloud speech', 'cloud language', 'cloud translation',
        'dialogflow', 'document ai', 'timeseries insights', 'ai notebooks', 'datalab',
        'heroku', 'digital ocean', 'linode', 'vultr', 'ibm cloud', 'oracle cloud', 'alibaba cloud',
        'tencent cloud', 'hetzner', 'scaleway', 'upcloud', 'exoscale', 'lenode', 'joyent', 'packet',

        # DevOps & Infrastructure (100+)
        'docker', 'kubernetes', 'k8s', 'helm', 'kustomize', 'kompose', 'docker compose', 'docker swarm',
        'containerization', 'container orchestration', 'podman', 'containerd', 'rkt', 'singularity',
        'jenkins', 'github actions', 'gitlab ci', 'circleci', 'travis ci', 'appveyor', 'buildkite',
        'drone', 'harness', 'spinnaker', 'argo', 'flux', 'tekton', 'gitops', 'weave', 'pulumi',
        'terraform', 'terraform cloud', 'ansible', 'puppet', 'chef', 'salt', 'cfn', 'bicep',
        'cloudformation', 'arm template', 'heat', 'tosca', 'jclouds', 'libcloud', 'fog',
        'terraform providers', 'terraform modules', 'terragrunt', 'terraspace', 'checkov', 'tflint',
        'prometheus', 'grafana', 'datadog', 'newrelic', 'dynatrace', 'elastic apm', 'splunk', 'sumo logic',
        'cloudwatch', 'stackdriver', 'azure monitor', 'application insights', 'honeycomb', 'lightstep',
        'jaeger', 'zipkin', 'datadog apm', 'signalfx', 'wavefront', 'moogsoft', 'vmware aria',
        'elk', 'elk stack', 'elasticsearch', 'logstash', 'kibana', 'beats', 'log4j', 'slf4j', 'logback',
        'winston', 'bunyan', 'pino', 'morgan', 'log4net', 'nlog', 'serilog', 'structlog',
        'vault', 'consul', 'secrets manager', 'key vault', 'kms', 'hsm', '1password', 'lastpass',
        'okta', 'auth0', 'keycloak', 'ldap', 'active directory', 'saml', 'oauth', 'oidc', 'jwt',
        'ssl', 'tls', 'ssh', 'gpg', 'pem', 'x509', 'certificate', 'pki', 'ca', 'eca',
        'nat', 'nat gateway', 'vpn', 'vpn gateway', 'wan', 'sd-wan', 'firewall', 'waf', 'ddos',
        'traefik', 'nginx', 'apache', 'caddy', 'envoy', 'linkerd', 'istio', 'service mesh', 'konga',
        'kong', 'tyk', 'apigee', 'aws api gateway', 'azure api management', 'google cloud apigee',
        'postman', 'insomnia', 'rest client', 'soap ui', 'jmeter', 'locust', 'gatling', 'neoload',
        'load testing', 'performance testing', 'stress testing', 'penetration testing', 'security testing',
        'sonarqube', 'checkmarx', 'fortify', 'veracode', 'qualys', 'rapid7', 'tenable', 'nessus',
        'owasp', 'bandit', 'snyk', 'dependabot', 'trivy', 'clair', 'anchore', 'grype',
        'sca', 'dast', 'sast', 'iast', 'rasp', 'cas', 'ciem', 'identity management', 'pam',
        'iaas', 'paas', 'saas', 'caas', 'faas', 'baas', 'dbaas', 'mbaas', 'vps', 'dedicated',

        # Mobile Development (80+)
        'ios', 'android', 'react native', 'flutter', 'swift', 'objective c', 'kotlin', 'java android',
        'xamarin', 'cordova', 'ionic', 'nativescript', 'unreal', 'unity', 'godot', 'corona',
        'phonegap', 'framework7', 'onsen ui', 'weex', 'quasar', 'ui kit', 'mobile ui', 'material design',
        'swiftui', 'combine', 'async await', 'concurrency', 'grand central dispatch', 'gcd', 'operationqueue',
        'jetpack', 'compose', 'kotlin coroutines', 'kotlin flow', 'livedata', 'viewmodel', 'room',
        'firebase', 'crashlytics', 'analytics', 'performance monitoring', 'test lab', 'app distribution',
        'appcenter', 'hockey app', 'testflight', 'fabric', 'branch', 'adjust', 'amplitude', 'mixpanel',
        'segment', 'appsflyer', 'singular', 'kochava', 'vserv', 'mobileaction', 'adjust', 'branch metrics',
        'xcode', 'android studio', 'visual studio app center', 'app store connect', 'google play console',
        'huawei appgallery', 'amazon appstore', 'samsung galaxy store', 'xiaomi getapps', 'oppo appmarket',
        'vivo appstore', 'meizu flyme', 'nokia app store', 'aptoide', 'f-droid', 'apkpure', 'apkcombo',

        # Desktop Applications (60+)
        'electron', 'qt', 'wxwidgets', 'gtk', 'tkinter', 'pyqt', 'pyside', 'dear imgui', 'imgui',
        'raylib', 'bgfx', 'gfxapi', 'vulkan', 'metal', 'opengl', 'directx', 'webgpu', 'webgl',
        'win32api', 'winapi', 'cocoa', 'appkit', 'uikit', 'x11', 'x window system', 'wayland',
        'gnome', 'kde', 'xfce', 'lxde', 'mate', 'cinnamon', 'unity', 'budgie', 'deepin',
        'tauri', 'wry', 'fltk', 'juce', 'cegui', 'gwen', 'mygui', 'quickgui', 'neoaxis',
        'cryengine', 'unreal engine', 'godot', 'unity', 'tiled', 'gamesalad', 'construct',

        # Game Development (70+)
        'unity', 'unreal engine', 'godot', 'cryengine', 'lumberyard', 'o3de', 'amazon lumberyard',
        'game development', 'game engine', 'graphics programming', 'game physics', 'collision detection',
        'physics engine', 'havok', 'nvidia physx', 'bullet', 'ode', 'newton dynamics', 'rapier',
        'bevy', 'amethyst', 'gfx-rs', 'vulkan', 'opengl', 'directx', 'webgpu', 'spirv',
        'shader', 'vertex shader', 'fragment shader', 'geometry shader', 'compute shader', 'tesselation',
        'hlsl', 'glsl', 'wgsl', 'metal', 'swift metal', 'directx hlsl', 'shader model',
        'gameplay', 'mechanics', 'level design', 'ai pathfinding', 'behavior tree', 'state machine',
        'animation', 'skeletal animation', 'blend shapes', 'motion capture', 'mocap', 'vicon',
        'optitrack', 'actor facial', 'facial capture', 'performance capture', 'volume capture',
        'particle system', 'vfx', 'visual effects', 'post processing', 'bloom', 'dof', 'motion blur',
        'ssao', 'ambient occlusion', 'ray tracing', 'path tracing', 'rtx', 'dlss', 'fsr', 'xess',

        # IoT & Embedded Systems (80+)
        'iot', 'embedded systems', 'firmware', 'microcontroller', 'mcu', 'arduino', 'raspberry pi',
        'esp8266', 'esp32', 'stm32', 'avr', 'pic', 'arm cortex', 'risc v', 'mips', 'powerpc',
        'rtos', 'embedded linux', 'yocto', 'buildroot', 'openembedded', 'uclinux', 'uclibc', 'musl',
        'tinyrtos', 'contiki', 'zephyr', 'riot', 'freertos', 'rtems', 'vxworks', 'qnx', 'integrity',
        'ros', 'ros2', 'gazebo', 'webots', 'coppeliasim', 'vrep', 'v-rep', 'coppelia simulation',
        'mqtt', 'coap', 'zigbee', 'zwave', 'lora', 'sigfox', 'nb iot', 'cat m1', 'cat m', 'lwm2m',
        'dtls', 'tls psk', 'jdwp', 'obd ii', 'can bus', 'lin bus', 'flexray', 'ethernet avb',
        'modbus', 'profibus', 'profinet', 'ethercat', 'powerlink', 'hart', 'foundation fieldbus',
        'serial communication', 'uart', 'spi', 'i2c', 'cxc', 'pwm', 'adc', 'dac', 'gpio',
        'sensor fusion', 'kalman filter', 'particle filter', 'inertial measurement', 'imu', 'ahrs',
        'gps', 'gnss', 'rtk', 'ppp', 'lidar', 'radar', 'sonar', 'camera', 'thermal imaging',
        'signal processing', 'dsp', 'fft', 'digital filtering', 'analog filtering', 'control systems',
        'pid control', 'state space', 'transfer function', 'laplace', 'z transform', 'bode plot',

        # Web3 & Blockchain (70+)
        'blockchain', 'bitcoin', 'ethereum', 'web3', 'defi', 'nft', 'token', 'smart contract',
        'solidity', 'vyper', 'web3.js', 'ethers.js', 'web3.py', 'web3j', 'web3.rb', 'web3.swift',
        'hardhat', 'truffle', 'brownie', 'foundry', 'dapptools', 'waffle', 'embark', 'ganache',
        'geth', 'infura', 'alchemy', 'quicknode', 'ankr', 'getblock', 'pocket network', 'pokt',
        'metamask', 'walletconnect', 'web3modal', 'web3 modal', 'magic link', 'privy', 'dynamic',
        'contractkit', 'web3 swift', 'web3 swift', 'web3swift', 'web3provider', 'json rpc',
        'layer 2', 'layer2', 'l2', 'rollup', 'optimistic rollup', 'zk rollup', 'zk snark',
        'plasma', 'state channel', 'payment channel', 'sidechains', 'bridge', 'cross chain',
        'polygon', 'arbitrum', 'optimism', 'zksync', 'starknet', 'scroll', 'mantle', 'linea',
        'zkensync', 'consensys', 'sequencer', 'prover', 'verifier', 'evm', 'evm compatible',
        'wasm', 'webassembly', 'wasm vm', 'cosmos', 'tendermint', 'solana', 'near', 'sui', 'aptos',
        'cardano', 'polkadot', 'substrate', 'ink', 'dapp', 'oracles', 'chainlink', 'band protocol',
        'uniswap', 'aave', 'compound', 'makerdao', 'yearn', 'curve', 'balancer', 'sushiswap',
        'liquidity pool', 'amm', 'constant product', 'concentrated liquidity', 'yield farming',
        'staking', 'yield aggregator', 'vault', 'strategy', 'governance', 'dao', 'multisig',
        'mev', 'flashbots', 'sandwich attack', 'front running', 'back running', 'atomic swap',

        # Data Engineering (100+)
        'data pipeline', 'etl', 'elt', 'data warehouse', 'data lake', 'data lakehouse', 'data mesh',
        'apache spark', 'spark', 'pyspark', 'spark sql', 'spark streaming', 'spark mllib',
        'hadoop', 'mapreduce', 'hdfs', 'hive', 'pig', 'sqoop', 'flume', 'hbase', 'kafka',
        'kafka connect', 'kafka streams', 'stream processing', 'event streaming', 'event driven',
        'apache flink', 'flink', 'storm', 'samza', 'beam', 'dataflow', 'pubsub', 'kinesis',
        'airflow', 'dag', 'orchestration', 'workflow', 'luigi', 'prefect', 'dagster', 'nextflow',
        'snakemake', 'makeflow', 'cctools', 'swift', 'pegasus', 'fireworks', 'parsl', 'ray', 'dask',
        'sql', 'bigquery', 'snowflake', 'redshift', 'athena', 'hive', 'presto', 'trino', 'impala',
        'clickhouse', 'vertica', 'exasol', 'netezza', 'greenplum', 'mariadb', 'oracle', 'ibm db2',
        'data quality', 'dbt', 'great expectations', 'soda', 'data contracts', 'schema registry',
        'data governance', 'metadata management', 'data lineage', 'data discovery', 'data catalog',
        'alation', 'collibra', 'informatica', 'talend', 'meltano', 'fivetran', 'stitch', 'rivery',
        'integration', 'data integration', 'api integration', 'webhook', 'cdc', 'change data capture',
        'binlog', 'wal', 'replication', 'sync', 'real time replication', 'log based cdc', 'query based',
        'query based cdc', 'table level capture', 'row level capture', 'logical decoding', 'wal decoding',
        'columnar storage', 'parquet', 'orc', 'arrow', 'iceberg', 'delta lake', 'hudi', 'lance',
        'compression', 'snappy', 'gzip', 'brotli', 'lz4', 'zstd', 'compression codec', 'encoding',
        'run length encoding', 'dictionary encoding', 'bit packing', 'rle', 'varint', 'zigzag',
        'partitioning', 'bucketing', 'sharding', 'distribution', 'consistent hashing', 'range partitioning',
        'hash partitioning', 'list partitioning', 'composite partitioning', 'partitioning strategy',
        'indexing', 'b tree', 'hash index', 'bitmap index', 'full text index', 'spatial index',
        'covering index', 'composite index', 'filtered index', 'partial index', 'expression index',
        'materialized view', 'cte', 'common table expression', 'window function', 'analytics',
        'olap', 'oltp', 'analytical processing', 'transactional processing', 'real time analytics',
        'business intelligence', 'bi', 'reporting', 'dashboarding', 'visualization', 'tableau',
        'power bi', 'looker', 'metabase', 'superset', 'grafana', 'kibana', 'qlik', 'cognos',

        # Software Architecture (80+)
        'microservices', 'monolithic', 'layered', 'hexagonal', 'onion', 'clean architecture',
        'mvc', 'mvp', 'mvvm', 'flux', 'redux', 'saga', 'observer', 'mediator', 'facade',
        'adapter', 'decorator', 'strategy', 'factory', 'abstract factory', 'singleton', 'builder',
        'prototype', 'bridge', 'composite', 'proxy', 'chain of responsibility', 'command',
        'interpreter', 'iterator', 'memento', 'state', 'template method', 'visitor', 'ddd',
        'cqrs', 'event sourcing', 'saga pattern', 'circuit breaker', 'retry', 'timeout', 'bulkhead',
        'rate limiting', 'throttling', 'backpressure', 'flow control', 'congestion control',
        'load balancing', 'round robin', 'least connection', 'ip hash', 'weighted', 'consistent hash',
        'service discovery', 'consul', 'eureka', 'zookeeper', 'etcd', 'dns sd', 'mcast',
        'api gateway', 'reverse proxy', 'load balancer', 'web server', 'application server',
        'message broker', 'message queue', 'pub sub', 'request reply', 'rpc', 'remoting',
        'distributed transaction', 'saga', 'two phase commit', 'distributed lock', 'consensus',
        'raft', 'paxos', 'byzantine fault tolerance', 'state machine replication', 'blockchain',
        'cache', 'caching', 'cache invalidation', 'cache coherence', 'cache eviction', 'ttl',
        'cdn', 'content delivery', 'edge computing', 'fog computing', 'cloudlet', 'mec',
        'serverless', 'functions as a service', 'faas', 'lambda', 'cloud functions', 'cloud run',
        'containers', 'orchestration', 'scheduling', 'provisioning', 'auto scaling', 'load shedding',
        'graceful degradation', 'fault tolerance', 'redundancy', 'replication', 'failover', 'disaster recovery',

        # Testing (100+)
        'unit testing', 'unit test', 'integration testing', 'integration test', 'system testing',
        'system test', 'acceptance testing', 'acceptance test', 'smoke testing', 'smoke test',
        'regression testing', 'regression test', 'sanity testing', 'sanity test', 'exploratory testing',
        'performance testing', 'performance test', 'load testing', 'load test', 'stress testing',
        'stress test', 'spike testing', 'soak testing', 'endurance testing', 'scalability testing',
        'volume testing', 'concurrency testing', 'longevity testing', 'reliability testing',
        'usability testing', 'user acceptance testing', 'uat', 'beta testing', 'alpha testing',
        'compatibility testing', 'browser testing', 'cross browser', 'responsive testing',
        'accessibility testing', 'a11y', 'wcag', 'aria', 'screen reader', 'keyboard navigation',
        'security testing', 'penetration testing', 'vulnerability assessment', 'threat modeling',
        'owasp', 'cwe', 'cve', 'cvss', 'severity', 'exploit', 'payload', 'injection', 'xss',
        'csrf', 'cors', 'clickjacking', 'sql injection', 'command injection', 'path traversal',
        'race condition', 'toctou', 'buffer overflow', 'format string', 'integer overflow',
        'zero day', 'exploit kit', 'malware', 'ransomware', 'worm', 'virus', 'trojan', 'spyware',
        'adware', 'rootkit', 'bootkit', 'firmware attack', 'supply chain attack', 'social engineering',
        'phishing', 'spear phishing', 'whaling', 'smishing', 'vishing', 'pretexting', 'baiting',
        'tdd', 'test driven development', 'bdd', 'behavior driven development', 'atdd',
        'acceptance test driven development', 'ddt', 'data driven testing', 'keyword driven',
        'fixture', 'setup', 'teardown', 'mock', 'mock object', 'stub', 'spy', 'fake', 'double',
        'test data', 'test data management', 'tdm', 'synthetic data', 'anonymization', 'masking',
        'pii', 'personally identifiable information', 'pci dss', 'hipaa', 'gdpr', 'ccpa',
        'pytest', 'unittest', 'nose', 'nose2', 'hypothesis', 'property based testing',
        'jest', 'mocha', 'jasmine', 'karma', 'qunit', 'testcafe', 'webdriverio', 'protractor',
        'cucumber', 'behat', 'behave', 'lettuce', 'robot', 'robot framework', 'fitnesse',
        'selenium', 'webdriver', 'appium', 'xctest', 'junit', 'testng', 'rest assured',
        'jmeter', 'locust', 'gatling', 'neoload', 'loadrunner', 'soapui', 'postman',
        'jacoco', 'cobertura', 'istanbul', 'nyc', 'coverage', 'code coverage', 'coverage report',
        'mutation testing', 'pitest', 'stryker', 'mutant', 'mutator', 'killed mutant',

        # Software Engineering Practices (80+)
        'scrum', 'agile', 'kanban', 'lean', 'xp', 'extreme programming', 'pair programming',
        'mob programming', 'swarmming', 'code review', 'peer review', 'pull request', 'pr',
        'merge request', 'mr', 'code quality', 'technical debt', 'refactoring', 'architecture decision',
        'adr', 'rfc', 'design document', 'architecture review board', 'arb', 'change advisory board',
        'cab', 'incident management', 'incident response', 'postmortem', 'blameless postmortem',
        'root cause analysis', 'rca', 'five whys', 'fishbone diagram', 'pareto analysis',
        'continuous integration', 'ci', 'continuous deployment', 'cd', 'continuous delivery',
        'continuous testing', 'continuous monitoring', 'continuous learning', 'devops',
        'gitops', 'infrastructure as code', 'iac', 'policy as code', 'paac', 'compliance as code',
        'observability', 'telemetry', 'logging', 'metrics', 'tracing', 'profiling', 'debugging',
        'performance optimization', 'optimization', 'bottleneck', 'profiler', 'flame graph',
        'version control', 'git', 'mercurial', 'subversion', 'cvs', 'perforce', 'git flow',
        'trunk based development', 'feature branch', 'release branch', 'hotfix', 'cherry pick',
        'rebase', 'merge', 'squash', 'conflict', 'merge conflict', 'conflict resolution',
        'documentation', 'api documentation', 'openapi', 'swagger', 'graphql schema', 'jsonschema',
        'javadoc', 'markdown', 'asciidoc', 'restructuredtext', 'sphinx', 'mkdocs', 'docusaurus',
        'changelog', 'semantic versioning', 'semver', 'versioning', 'backward compatibility',
        'deprecation', 'sunset', 'migration', 'upgrade', 'downgrade', 'rollback', 'deployment',
        'blue green', 'canary', 'shadow', 'dark', 'feature flag', 'feature toggle', 'experiment',
        'a/b testing', 'multivariate testing', 'split testing', 'batch size', 'lead time',
        'deployment frequency', 'change failure rate', 'mttr', 'mttf', 'availability', 'reliability',
        'resilience', 'scalability', 'capacity', 'qos', 'sla', 'slo', 'slb', 'service level',

        # Cloud-Native & Distributed (80+)
        'cloud native', 'cncf', 'cloud native computing', 'cncd', '12factor', '12 factor app',
        'containers', 'docker', 'podman', 'containerd', 'rkt', 'lxc', 'lxd', 'opencontainers',
        'oci', 'image spec', 'runtime spec', 'distribution spec', 'cnab', 'docker hub',
        'registry', 'container registry', 'artifactory', 'nexus', 'ecr', 'acr', 'gcr',
        'kubernetes', 'k8s', 'pod', 'deployment', 'statefulset', 'daemonset', 'job', 'cronjob',
        'service', 'ingress', 'network policy', 'security policy', 'resource quota', 'limit range',
        'configmap', 'secret', 'volume', 'persistent volume', 'pv', 'persistent volume claim',
        'pvc', 'storage class', 'dynamic provisioning', 'static provisioning', 'hostpath', 'emptydir',
        'helm', 'chart', 'helm chart', 'helm repository', 'chartmuseum', 'harbor', 'plugin',
        'helmfile', 'kustomize', 'kustomization', 'patch', 'overlay', 'base', 'jsonpatch',
        'operator', 'crd', 'custom resource definition', 'admission controller', 'mutating webhook',
        'validating webhook', 'rbac', 'role based access control', 'clusterrole', 'clusterrolebinding',
        'role', 'rolebinding', 'serviceaccount', 'user', 'group', 'authentication', 'authorization',
        'pod security policy', 'psp', 'pod security admission', 'psa', 'network policy',
        'istio', 'service mesh', 'linkerd', 'consul', 'kuma', 'traefik', 'kong', 'gravitee',
        'virtual service', 'destination rule', 'gateway', 'peer authentication', 'request authentication',
        'telemetry', 'metrics', 'tracing', 'logging', 'monitoring', 'observability', 'o11y',
        'distributed tracing', 'apm', 'application performance monitoring', 'rum', 'real user monitoring',
        'synthetic monitoring', 'proactive monitoring', 'reactive monitoring', 'predictive analytics',
        'machine learning ops', 'mlops', 'modelops', 'dataops', 'analytics engineering',

        # Civil Engineering (60+)
        'civil engineering', 'structural engineering', 'geotechnical', 'hydraulic', 'water resources',
        'transportation', 'highway', 'railway', 'bridge', 'tunnel', 'dam', 'irrigation',
        'drainage', 'sewage', 'wastewater', 'stormwater', 'cad', 'revit', 'autocad', '3d modeling',
        'bim', 'building information modeling', 'tekla', 'bentley', 'civil 3d', 'navisworks',
        'fem', 'finite element', 'fea', 'finite element analysis', 'cfm', 'computational fluid',
        'cfd', 'computational fluid dynamics', 'structural analysis', 'stress analysis', 'strain',
        'loading', 'foundation', 'soil mechanics', 'consolidation', 'settlement', 'bearing capacity',
        'slope stability', 'retaining wall', 'earthquake', 'seismic', 'tsunami', 'liquefaction',
        'concrete', 'steel', 'timber', 'masonry', 'composite', 'reinforced concrete', 'rc',
        'prestressed concrete', 'pc', 'asphalt', 'pavement', 'quality control', 'testing',

        # Mechanical Engineering (80+)
        'mechanical engineering', 'thermodynamics', 'dynamics', 'kinematics', 'statics', 'mechanics',
        'material science', 'materials', 'creep', 'fatigue', 'fracture', 'brittle', 'ductile',
        'yield strength', 'ultimate strength', 'tensile', 'compressive', 'shear', 'torsion',
        'vibration', 'harmonic', 'resonance', 'damping', 'frequency', 'natural frequency',
        'manufacturing', 'machining', 'casting', 'forging', 'welding', 'joining', 'assembly',
        'tolerances', 'gd&t', 'geometric dimensioning', 'surface finish', 'roughness', 'flatness',
        'precision', 'accuracy', 'repeatability', 'reproducibility', 'measurement', 'inspection',
        'cad', 'solidworks', 'creo', 'catia', 'nx', 'fusion 360', '3d modeling', 'part design',
        'surfacing', 'sheet metal', 'weldments', 'motion', 'mechanism', 'drivetrain', 'gears',
        'bearings', 'friction', 'lubrication', 'sealing', 'pneumatic', 'hydraulic', 'fluid power',
        'control', 'feedback', 'pid', 'automation', 'plc', 'programmable logic controller', 'scada',
        'hvac', 'heating', 'ventilation', 'air conditioning', 'thermal comfort', 'indoor air quality',
        'iaq', 'acoustics', 'noise', 'vibration', 'harshness', 'nvh', 'ergonomics', 'human factors',
        'quality assurance', 'qa', 'six sigma', 'lean manufacturing', 'kaizen', 'just in time', 'jit',
        'robotics', 'robot', 'automation', 'actuator', 'motor', 'sensor', 'transducer',

        # Electrical Engineering (100+)
        'electrical engineering', 'power systems', 'power generation', 'transmission', 'distribution',
        'smart grid', 'microgrid', 'nanogrid', 'grid', 'phasor', 'synchrophasor', 'wami',
        'renewable energy', 'solar', 'pv', 'photovoltaic', 'wind', 'hydroelectric', 'tidal',
        'geothermal', 'biomass', 'nuclear', 'fossil fuel', 'coal', 'natural gas', 'lng',
        'power electronics', 'converter', 'inverter', 'rectifier', 'transformer', 'switchgear',
        'circuit breaker', 'relay', 'protection', 'grounding', 'earthing', 'lightning', 'surge',
        'motor', 'generator', 'turbine', 'compressor', 'pump', 'fan', 'rotary machine',
        'induction motor', 'synchronous motor', 'stepper motor', 'brushless dc', 'bldc', 'ac dc',
        'power factor', 'reactive power', 'harmonic', 'distortion', 'thd', 'total harmonic',
        'transient', 'steady state', 'stability', 'frequency', 'voltage', 'current', 'impedance',
        'circuit analysis', 'network analysis', 'mesh analysis', 'nodal analysis', 'superposition',
        'thevenin', 'norton', 'maximum power transfer', 'resonance', 'bandwidth', 'quality factor',
        'filter', 'low pass', 'high pass', 'band pass', 'band stop', 'notch', 'butterworth',
        'chebyshev', 'bessel', 'elliptic', 'analog', 'digital', 'fir', 'iir', 'kalman',
        'signal processing', 'dsp', 'fourier', 'fft', 'convolution', 'correlation', 'autocorrelation',
        'cross correlation', 'wavelet', 'time frequency', 'stft', 'spectrogram', 'waterfall',
        'control', 'system', 'feedback', 'feedforward', 'cascade', 'pid', 'lead lag', 'compensator',
        'observer', 'state feedback', 'linear quadratic', 'lq', 'lqr', 'optimal control', 'mpc',
        'model predictive control', 'robust control', 'h infinity', 'mu synthesis', 'adaptive control',
        'neural network', 'fuzzy logic', 'genetic algorithm', 'particle swarm', 'ant colony',
        'electromagnetics', 'em', 'maxwell', 'faraday', 'ampere', 'gauss', 'biot savart',
        'electric field', 'magnetic field', 'electromagnetic field', 'emf', 'inductance', 'capacitance',
        'resistance', 'conductance', 'susceptance', 'reluctance', 'permeability', 'permittivity',
        'dielectric', 'conductor', 'semiconductor', 'superconductor', 'ferrite', 'ferrofluid',
        'communication', 'transmission line', 'waveguide', 'antenna', 'dipole', 'monopole', 'array',
        'phased array', 'mimo', 'beamforming', 'modulation', 'am', 'fm', 'pm', 'psk', 'qam',
        'ofdm', 'ofdma', 'spread spectrum', 'cdma', 'tdma', 'fdma', 'sdma', 'multiple access',
        'channel', 'fading', 'rayleigh', 'rician', 'awgn', 'path loss', 'shadowing', 'multipath',
        'coding', 'error correction', 'ecc', 'hamming', 'reed solomon', 'turbo', 'ldpc', 'polar',
        'encryption', 'rsa', 'dsa', 'ecc', 'aes', 'des', 'hash', 'sha', 'md5', 'blockchain',

        # Chemical Engineering (70+)
        'chemical engineering', 'process', 'unit operation', 'transport phenomena', 'heat transfer',
        'mass transfer', 'momentum transfer', 'fluid mechanics', 'fluid dynamics', 'hydraulic',
        'thermodynamics', 'reaction', 'kinetics', 'catalysis', 'equilibrium', 'phase equilibrium',
        'vapor liquid', 'vle', 'liquid liquid', 'lle', 'solid liquid', 'sle', 'fugacity',
        'activity', 'ideal solution', 'non ideal', 'mixing', 'separation', 'distillation',
        'absorption', 'adsorption', 'extraction', 'crystallization', 'precipitation', 'filtration',
        'settling', 'centrifugation', 'evaporation', 'drying', 'membrane', 'osmosis', 'dialysis',
        'electrodialysis', 'ion exchange', 'chromatography', 'spectroscopy', 'spectrometry',
        'analyzer', 'detector', 'chromatograph', 'reactor', 'batch', 'continuous', 'plug flow',
        'pfr', 'cstr', 'stirred tank', 'selectivity', 'yield', 'conversion', 'residence time',
        'contact time', 'residence', 'mixing', 'agitation', 'turbulence', 'reynolds', 'froude',
        'froude number', 'power number', 'dimensionless', 'scaling', 'scale up', 'pilot plant',
        'quality control', 'qc', 'quality assurance', 'qa', 'specification', 'gmp', 'good manufacturing',
        'cGMP', 'compliance', 'validation', 'iq', 'oq', 'pq', 'iqoqpq', 'csv', 'computer system',
        'environmental', 'sustainability', 'green chemistry', 'bio based', 'circular economy',
        'waste', 'waste treatment', 'pollutant', 'emission', 'effluent', 'remediation',
        'pharmaceutical', 'drug', 'active pharmaceutical', 'api', 'excipient', 'formulation',
        'biotech', 'biotechnology', 'fermentation', 'bioreactor', 'microbiology', 'cell culture',

        # Aerospace Engineering (80+)
        'aerospace engineering', 'aerodynamics', 'aeronautics', 'astronautics', 'flight', 'aircraft',
        'helicopter', 'rotor', 'wing', 'fuselage', 'tail', 'empennage', 'control surface', 'aileron',
        'elevator', 'rudder', 'flap', 'slat', 'spoiler', 'airfoil', 'naca', 'camber', 'thickness',
        'angle of attack', 'aoa', 'alpha', 'chord', 'span', 'aspect ratio', 'ar', 'taper ratio',
        'sweep', 'dihedral', 'toe in', 'washout', 'induced drag', 'profile drag', 'parasitic drag',
        'wave drag', 'skin friction', 'pressure drag', 'vortex', 'wake', 'circulation', 'lift',
        'drag', 'pitching moment', 'yawing moment', 'rolling moment', 'stability', 'controllability',
        'trim', 'equilibrium', 'dynamic stability', 'static stability', 'divergence', 'flutter',
        'buffeting', 'whirl', 'divergence speed', 'flutter speed', 'mach', 'sonic', 'supersonic',
        'hypersonic', 'transonic', 'transonic flow', 'shock', 'boundary layer', 'separation',
        'reattachment', 'stall', 'spin', 'autorotation', 'cfd', 'wind tunnel', 'tunnel test',
        'engine', 'jet', 'turbofan', 'turboshaft', 'turbojet', 'turboprop', 'piston', 'propeller',
        'thrust', 'specific impulse', 'isp', 'fuel consumption', 'sfc', 'specific fuel consumption',
        'combustion', 'burner', 'combustor', 'exhaust', 'nozzle', 'afterburner', 'reheat',
        'compressor', 'compressor map', 'stall', 'surge', 'pressure ratio', 'turbine', 'rotor blade',
        'stator', 'clearance', 'seal', 'bearing', 'vibration', 'resonance', 'bending', 'torsion',
        'structure', 'fuselage', 'wing structure', 'spar', 'rib', 'skin', 'stiffener', 'fastener',
        'composite', 'layup', 'fiber', 'matrix', 'resin', 'carbon', 'glass', 'aramid', 'boron',
        'sandwich', 'honeycomb', 'foam', 'core', 'face sheet', 'ply', 'weave', 'fiber orientation',
        'stress', 'strain', 'fatigue', 'creep', 'corrosion', 'environmental', 'moisture', 'salt fog',
        'maintenance', 'inspection', 'nondestructive', 'ndt', 'ultrasonic', 'x-ray', 'thermography',
        'systems', 'hydraulic', 'pneumatic', 'electrical', 'fuel', 'environmental control', 'ecs',
        'avionics', 'navigation', 'communication', 'autopilot', 'flight management', 'fms', 'fly by wire',
        'guidance', 'propulsion', 'mission', 'flight plan', 'trajectory', 'cruise', 'descent',
        'landing', 'takeoff', 'climb', 'maximum altitude', 'ceiling', 'range', 'endurance',
        'performance', 'payload', 'center of gravity', 'cg', 'moment', 'center of pressure', 'cp',
        'neutral point', 'static margin', 'dynamic margin', 'handling qualities', 'hq', 'flying qualities',

        # Material Science (70+)
        'material science', 'materials engineering', 'metallurgy', 'polymer', 'ceramic', 'composite',
        'alloy', 'phase diagram', 'binary', 'ternary', 'quaternary', 'multi component', 'phase',
        'phase boundary', 'solid solution', 'substitution', 'interstitial', 'compound', 'intermetallic',
        'grain', 'grain boundary', 'grain size', 'grain growth', 'recrystallization', 'recovery',
        'crystal', 'crystallography', 'crystal structure', 'lattice', 'unit cell', 'bravais',
        'miller indices', 'slip', 'slip plane', 'slip direction', 'dislocation', 'line dislocation',
        'edge dislocation', 'screw dislocation', 'burgers vector', 'stacking fault', 'twinning',
        'point defect', 'vacancy', 'interstitial', 'frenkel', 'schottky', 'antisite', 'dopant',
        'diffusion', 'fick', 'activation energy', 'arrhenius', 'grain boundary diffusion', 'surface diffusion',
        'mechanical properties', 'elasticity', 'plasticity', 'viscoelasticity', 'elastic modulus',
        'youngs modulus', 'shear modulus', 'bulk modulus', 'hardness', 'toughness', 'brittleness',
        'ductility', 'malleability', 'resilience', 'strain hardening', 'work hardening', 'annealing',
        'thermal properties', 'thermal conductivity', 'thermal expansion', 'specific heat', 'melting point',
        'glass transition', 'tg', 'crystallization', 'sintering', 'densification', 'porosity',
        'electrical properties', 'conductivity', 'resistivity', 'semiconductor', 'dopant', 'carrier',
        'hole', 'electron', 'acceptor', 'donor', 'bandgap', 'fermi level', 'fermi surface',
        'optical properties', 'absorption', 'transmission', 'reflection', 'refraction', 'refractive index',
        'birefringence', 'dichroism', 'fluorescence', 'phosphorescence', 'luminescence', 'color',
        'magnetic properties', 'diamagnetic', 'paramagnetic', 'ferromagnetic', 'antiferromagnetic',
        'ferrimagnetic', 'curie', 'saturation', 'magnetization', 'permeability', 'susceptibility',
        'processing', 'casting', 'forging', 'rolling', 'extrusion', 'drawing', 'stamping', 'forming',
        'powder metallurgy', 'sintering', 'pressing', 'heat treatment', 'quenching', 'tempering',
        'case hardening', 'carburizing', 'nitriding', 'surface treatment', 'coating', 'plating',

        # Environmental Engineering (80+)
        'environmental engineering', 'water treatment', 'wastewater treatment', 'air quality',
        'noise pollution', 'solid waste', 'hazardous waste', 'recycling', 'remediation', 'cleanup',
        'soil pollution', 'groundwater', 'surface water', 'marine', 'estuary', 'coastal', 'wetland',
        'ecosystem', 'biodiversity', 'habitat', 'conservation', 'preservation', 'restoration',
        'water', 'drinking water', 'potable water', 'saltwater', 'brackish', 'desalination', 'reverse osmosis',
        'ro', 'nanofiltration', 'nf', 'ultrafiltration', 'uf', 'microfiltration', 'mf', 'membrane',
        'clarification', 'coagulation', 'flocculation', 'sedimentation', 'settling', 'flotation',
        'disinfection', 'chlorination', 'ozonation', 'uv', 'ultraviolet', 'advanced oxidation', 'aop',
        'ion exchange', 'softening', 'hardness', 'alkalinity', 'acidity', 'ph', 'buffer', 'corrosion',
        'scale', 'fouling', 'biofouling', 'biofilm', 'legionella', 'cryptosporidium', 'giardia',
        'bacteria', 'virus', 'protozoa', 'pathogen', 'indicator organism', 'mpn', 'cfu', 'tds',
        'tss', 'bod', 'cod', 'toc', 'doe', 'discharge', 'loadings', 'nutrients', 'nitrogen',
        'phosphorus', 'eutrophication', 'algae', 'algal bloom', 'dead zone', 'hypoxia', 'anoxia',
        'nitrification', 'denitrification', 'anammox', 'phosphorus recovery', 'struvite', 'aeration',
        'aerobic', 'anaerobic', 'facultative', 'microorganism', 'biomass', 'sludge', 'biosolids',
        'composting', 'vermicomposting', 'anaerobic digestion', 'methane', 'biogas', 'energy recovery',
        'combustion', 'incineration', 'gasification', 'pyrolysis', 'carbonization', 'landfill',
        'leachate', 'gas', 'liner', 'cap', 'closure', 'post closure', 'monitoring', 'emissions',
        'air', 'pollutant', 'criteria pollutant', 'pm', 'pm2.5', 'pm10', 'nox', 'sox', 'co', 'o3',
        'volatile organic', 'voc', 'hazardous air pollutant', 'hap', 'pah', 'pcb', 'dioxin',
        'stack', 'scrubber', 'baghouse', 'electrostatic precipitator', 'esp', 'selective catalytic',
        'scr', 'nh3', 'urea', 'ash', 'fly ash', 'bottom ash', 'recovery', 'reuse', 'cement',
        'climate', 'greenhouse', 'ghg', 'co2', 'ch4', 'n2o', 'carbon', 'carbon sequestration',
        'carbon offset', 'renewable', 'efficiency', 'conservation', 'sustainable', 'lca', 'life cycle',

        # Non-Technical Professional Skills (100+)
        'project management', 'pm', 'scope', 'schedule', 'budget', 'resource', 'risk', 'quality',
        'communication', 'stakeholder', 'team management', 'leadership', 'motivation', 'delegation',
        'conflict resolution', 'negotiation', 'problem solving', 'critical thinking', 'analytical',
        'decision making', 'strategic thinking', 'planning', 'organization', 'time management',
        'prioritization', 'prioritize', 'efficiency', 'productivity', 'work ethic', 'discipline',
        'attention to detail', 'accuracy', 'precision', 'reliability', 'accountability', 'responsibility',
        'initiative', 'proactive', 'adaptability', 'flexibility', 'resilience', 'perseverance',
        'learning', 'continuous learning', 'self improvement', 'personal development', 'growth mindset',
        'collaboration', 'teamwork', 'cooperation', 'synergy', 'partnership', 'alliance', 'coalition',
        'networking', 'relationship building', 'interpersonal', 'empathy', 'emotional intelligence',
        'eq', 'persuasion', 'influence', 'presentation', 'public speaking', 'communication skills',
        'writing', 'technical writing', 'documentation', 'report', 'proposal', 'business case',
        'analysis', 'data analysis', 'trend analysis', 'forecasting', 'reporting', 'visualization',
        'business acumen', 'financial', 'economics', 'roi', 'return on investment', 'bottom line',
        'revenue', 'cost', 'profit', 'margin', 'budgeting', 'forecasting', 'scenario planning',
        'sales', 'marketing', 'customer', 'client', 'account management', 'retention', 'growth',
        'innovation', 'creativity', 'ideation', 'brainstorming', 'thinking outside the box',
        'change management', 'transformation', 'change leadership', 'adoption', 'resistance',
        'vendor management', 'procurement', 'contracts', 'compliance', 'governance', 'audit',
        'quality assurance', 'qa', 'continuous improvement', 'kaizen', 'lean', 'six sigma',
        'process improvement', 'optimization', 'automation', 'workflow', 'efficiency', 'effectiveness',
        'training', 'coaching', 'mentoring', 'teaching', 'knowledge transfer', 'documentation',
        'problem solving', 'root cause', 'troubleshooting', 'debugging', 'investigative', 'analytical',
        'strategic planning', 'vision', 'mission', 'goals', 'objectives', 'kpi', 'metrics',
        'cross functional', 'cross discipline', 'interdisciplinary', 'holistic', 'systems thinking',
        'big picture', 'long term', 'short term', 'planning horizon', 'roadmap', 'milestone',
        'business writing', 'executive summary', 'abstract', 'brief', 'concise', 'clear', 'conciseness',
        'diplomacy', 'tact', 'political', 'office politics', 'organizational dynamics', 'culture',
        'ethics', 'integrity', 'honesty', 'transparency', 'trustworthiness', 'credibility',
        'customer focus', 'user centric', 'design thinking', 'lean startup', 'agile mindset',
        'business development', 'bd', 'partnerships', 'strategic alliance', 'joint venture',
        'market analysis', 'competitive', 'competitor', 'benchmark', 'best practice', 'industry',
        'risk management', 'mitigation', 'contingency', 'business continuity', 'disaster recovery',
        'quality', 'excellence', 'best in class', 'industry standard', 'compliance', 'regulation',
    }

    # Split by various delimiters and clean
    text = resume_text.lower()
    # Replace common delimiters with commas
    text = re.sub(r'[•·\-—|]', ',', text)
    text = re.sub(r'[\/]', ' ', text)

    # Split into tokens
    tokens = re.split(r'[,\n;]+', text)

    skills = []
    seen = set()

    for token in tokens:
        # Clean the token
        token = token.strip()
        # Remove special chars but keep +, #, -
        token = re.sub(r'[^\w\s+#\-.]', '', token)
        token = token.strip()

        # Skip if too short, empty, or is a number
        if not token or len(token) < 2 or token.isdigit():
            continue

        # Skip if it's a common stopword
        if token.lower() in stopwords:
            continue

        # Skip if it's purely numbers with dots (like versions)
        if re.match(r'^[\d.]+$', token):
            continue

        # Keep if it's a known technical skill
        if token.lower() in technical_keywords:
            if token.lower() not in seen:
                seen.add(token.lower())
                skills.append(token)
        # Keep multi-word terms that don't look generic
        elif ' ' in token or '+' in token or len(token) > 4:
            # Check if it contains at least one technical keyword or is capitalized (likely a proper term)
            if any(keyword in token.lower() for keyword in technical_keywords) or token[0].isupper():
                if token.lower() not in seen:
                    seen.add(token.lower())
                    skills.append(token)
        # Keep single technical-looking words (with numbers or special chars like C++)
        elif (len(token) <= 4 and (token[0].isupper() or '+' in token or '#' in token)) or \
                any(keyword in token.lower() for keyword in technical_keywords):
            if token.lower() not in seen:
                seen.add(token.lower())
                skills.append(token)

    return skills[:25]  # Limit to top 25 most relevant skills


def make_api_request(endpoint: str, payload: dict, method: str = "POST") -> Optional[dict]:
    """
    Make API request with error handling.

    Args:
        endpoint: API endpoint (e.g., "/skill-gap")
        payload: Request payload
        method: HTTP method (POST, GET)

    Returns:
        Response JSON or None if error
    """
    try:
        url = f"{BACKEND_URL}{endpoint}"

        if method == "POST":
            response = requests.post(
                url, json=payload, timeout=REQUEST_TIMEOUT)
        else:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 422:
            st.error(f"❌ Invalid input: {response.json()}")
            return None
        elif response.status_code >= 500:
            st.error("❌ Backend server error. Please try again later.")
            logger.error(f"Backend error: {response.status_code}")
            return None
        else:
            st.error(f"❌ API Error: {response.status_code}")
            return None

    except requests.Timeout:
        st.error("⏱️ Request timed out. Backend might be slow. Please try again.")
        logger.error(f"Request timeout to {url}")
        return None
    except requests.ConnectionError:
        st.error(
            f"🔌 Cannot connect to backend at {BACKEND_URL}. Is it running?")
        logger.error(f"Connection error to {BACKEND_URL}")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Unexpected error: {e}")
        return None


# ==============================
# Sidebar - Configuration & Info
# ==============================

with st.sidebar:
    st.header("⚙️ Configuration")

    # Backend status
    if check_backend_health():
        st.success("✅ Backend connected")
    else:
        st.error("❌ Backend not available")
        st.info(f"Connect to: {BACKEND_URL}")

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        """
        SkillBridge-AI helps you:
        - Identify skill gaps for target roles
        - Get personalized learning paths
        - Understand why skills matter
        """
    )

# ==============================
# Main Content - Candidate Input
# ==============================

st.header("👤 Candidate Profile")

col1, col2 = st.columns(2)

with col1:
    candidate_name = st.text_input(
        "Candidate Name",
        placeholder="Enter your name",
        help="Your full name or identifier"
    )
    current_role = st.text_input(
        "Current Role",
        placeholder="e.g., Junior Developer",
        help="Your current job title"
    )

with col2:
    experience_years = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=70,
        value=2,
        help="Total years of professional experience"
    )

# Resume upload with skill extraction
st.subheader("📄 Skills Input")

tab1, tab2 = st.tabs(["Upload Resume (PDF)", "Manual Skills Entry"])

skills_list = []

# Initialize session state for resume text
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""

with tab1:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        help="Upload a PDF resume to auto-extract skills"
    )

    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = "\n".join(
                    [page.extract_text() or "" for page in pdf.pages]
                )

            # Store in session state for later use
            st.session_state.resume_text = resume_text

            st.success("✅ PDF parsed successfully")

            with st.expander("View extracted text", expanded=False):
                st.text_area(
                    "Extracted Resume Text",
                    resume_text,
                    height=200,
                    disabled=True
                )

            # Auto-extract skills
            skills_list = parse_resume_text(resume_text)
            st.info(f"📌 Extracted {len(skills_list)} potential skills")

        except Exception as e:
            st.error(f"❌ Error parsing PDF: {str(e)}")
            logger.error(f"PDF parsing error: {e}")
    else:
        st.info("👆 Upload a PDF resume to extract skills automatically")

with tab2:
    skills_input = st.text_area(
        "Enter Skills (comma or newline separated)",
        placeholder="e.g., Python, SQL, Docker\nMachine Learning, Pandas",
        help="Enter skills manually, separated by commas or newlines"
    )

    if skills_input:
        skills_list = [s.strip() for s in skills_input.replace(
            "\n", ",").split(",") if s.strip()]

# Display skills with selection UI
if skills_list:
    st.subheader(f"✅ Extracted Skills ({len(skills_list)})")

    # Create columns for better layout
    st.info(
        "📋 Review and select the relevant skills below. Deselect any that don't apply:")

    # Use session state to track selected skills
    if 'selected_skills' not in st.session_state:
        st.session_state.selected_skills = {
            skill: True for skill in skills_list}

    # Display skills in a grid layout with checkboxes
    cols = st.columns(3)
    col_idx = 0

    for skill in skills_list:
        with cols[col_idx % 3]:
            st.session_state.selected_skills[skill] = st.checkbox(
                skill,
                value=st.session_state.selected_skills.get(skill, True),
                key=f"skill_{skill}"
            )
        col_idx += 1

    # Get only selected skills
    final_skills_list = [
        skill for skill, selected in st.session_state.selected_skills.items() if selected]

    # Show summary
    st.divider()
    st.success(
        f"✅ {len(final_skills_list)} skills selected out of {len(skills_list)} extracted")

    if len(final_skills_list) == 0:
        st.warning("⚠️ Please select at least one skill to continue")

else:
    st.warning("⚠️ No skills provided. Upload a resume or enter skills manually.")
    final_skills_list = []

# ==============================
# Target Job Section
# ==============================

st.header("🎯 Target Job")

target_job = st.text_input(
    "Target Job Role",
    value="Machine Learning Engineer",
    placeholder="e.g., Data Scientist, Backend Engineer",
    help="The job role you're targeting"
)

# ==============================
# Job Description Section (New)
# ==============================

st.header("📋 Job Description Analysis")

st.info("💡 Paste the job description to get a detailed AI analysis of your match and improvement areas")

job_description = st.text_area(
    "Paste Job Description",
    placeholder="Paste the complete job description here...\n\nInclude:\n- Job title and responsibilities\n- Required skills and experience\n- Nice-to-have qualifications",
    height=150,
    help="Provide the full job description for accurate analysis"
)

# ==============================
# Analysis Section
# ==============================

st.header("📊 Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    analyze_btn = st.button("🔍 Analyze Skill Gap", use_container_width=True)

with col2:
    learning_btn = st.button("📚 Generate Learning Path",
                             use_container_width=True)

with col3:
    explain_btn = st.button("💡 Get AI Explanation", use_container_width=True)

# Job Description Analysis Button (New Row)
st.divider()
st.subheader("🎯 Job Match Analysis")

job_match_btn = st.button("🔥 Analyze Job Match with AI",
                          use_container_width=True, type="primary")

# Validate inputs
if not candidate_name:
    st.warning("⚠️ Please enter your name")
elif not final_skills_list:
    st.warning("⚠️ Please select at least one skill")
elif not target_job:
    st.warning("⚠️ Please enter a target job role")
else:
    # Skill Gap Analysis
    if analyze_btn:
        payload = {
            "candidate": {
                "name": candidate_name,
                "current_role": current_role,
                "skills": final_skills_list,
                "experience_years": experience_years
            },
            "target_job": target_job
        }

        with st.spinner("🔄 Analyzing skill gap..."):
            result = make_api_request("/skill-gap", payload)

        if result:
            st.success("✅ Analysis complete!")

            # Metrics
            matched = result.get("matched_skills", [])
            missing = result.get("missing_skills", [])
            match_pct = result.get("match_percentage", 0)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Matched Skills", len(matched))
            with col2:
                st.metric("Missing Skills", len(missing))
            with col3:
                st.metric("Match %", f"{match_pct}%")

            # Visualization
            if matched or missing:
                skill_data = pd.DataFrame({
                    "Status": ["Matched", "Missing"],
                    "Count": [len(matched), len(missing)]
                })
                chart = alt.Chart(skill_data).mark_bar().encode(
                    x=alt.X("Status:N", axis=alt.Axis(labelAngle=0)),
                    y="Count:Q",
                    color=alt.Color("Status:N", scale=alt.Scale(scheme="set2"))
                ).properties(title="Skill Comparison", height=300)
                st.altair_chart(chart, use_container_width=True)

            # Skill lists
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")
                if matched:
                    for skill in matched:
                        st.write(f"• {skill}")
                else:
                    st.info("No matched skills yet")

            with col2:
                st.subheader("❌ Missing Skills")
                if missing:
                    for skill in missing:
                        st.write(f"• {skill}")
                else:
                    st.success("All required skills matched!")

    # Learning Path Generation
    if learning_btn:
        payload = {
            "candidate": {
                "name": candidate_name,
                "current_role": current_role,
                "skills": final_skills_list,
                "experience_years": experience_years
            },
            "target_job": target_job
        }

        with st.spinner("📚 Generating learning path..."):
            result = make_api_request("/learning-path", payload)

        if result:
            st.success("✅ Learning path created!")

            plan = result.get("learning_plan", [])
            total_weeks = result.get("total_weeks", 0)

            st.metric("Total Duration", f"{total_weeks} weeks")

            # Create timeline visualization
            if plan:
                plan_df = pd.DataFrame(plan)

                timeline_chart = alt.Chart(plan_df).mark_bar().encode(
                    x=alt.X("start_week:Q", title="Start Week"),
                    x2="end_week:Q",
                    y=alt.Y("skill:N", title="Skill"),
                    color=alt.Color(
                        "level:N", scale=alt.Scale(scheme="viridis")),
                    tooltip=["skill", "level", "start_week", "end_week"]
                ).properties(
                    title="Learning Roadmap",
                    height=400
                )
                st.altair_chart(timeline_chart, use_container_width=True)

                # Detailed steps
                st.subheader("📋 Learning Steps")
                for idx, row in plan_df.iterrows():
                    with st.expander(f"Week {row['start_week']}: {row['skill']} ({row['level']})"):
                        st.write(
                            f"**Duration:** Week {row['start_week']} - {row['end_week']}")
                        st.write(f"**Level:** {row['level']}")
                        if row.get("resources"):
                            st.write("**Resources:**")
                            for resource in row["resources"]:
                                st.write(f"- {resource}")

    # LLM Explanation
    if explain_btn:
        payload = {
            "candidate": {
                "name": candidate_name,
                "current_role": current_role,
                "skills": final_skills_list,
                "experience_years": experience_years
            },
            "target_job": target_job
        }

        with st.spinner("💭 Generating AI explanation..."):
            result = make_api_request("/skill-gap-llm", payload)

        if result:
            st.success("✅ AI analysis ready!")

            # Show LLM explanation
            st.subheader("💡 AI Reasoning")
            explanation = result.get(
                "llm_explanation", "No explanation available")
            st.write(explanation)

            # Show missing skills identified
            missing_skills = result.get("missing_skills", [])
            if missing_skills:
                st.subheader("🎯 Key Skills to Develop")
                cols = st.columns(min(3, len(missing_skills)))
                for idx, skill in enumerate(missing_skills):
                    with cols[idx % len(cols)]:
                        st.info(skill)

    # Job Description Match Analysis (New)
    if job_match_btn:
        if not job_description or job_description.strip() == "":
            st.error("❌ Please paste a job description to analyze")
        elif not st.session_state.resume_text:
            st.error(
                "❌ Please upload a resume first to compare with job description")
        else:
            payload = {
                "candidate_name": candidate_name,
                "current_role": current_role,
                "experience_years": experience_years,
                "resume_text": st.session_state.resume_text,
                "target_job": target_job,
                "job_description": job_description
            }

            with st.spinner("🔄 Analyzing job match with AI..."):
                result = make_api_request("/job-match", payload)

            if result:
                st.success("✅ Job match analysis complete!")

                # Create tabs for different analyses
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Match Score",
                    "🎯 Areas to Improve",
                    "📚 Learning Plan",
                    "💡 AI Insights"
                ])

                with tab1:
                    st.subheader("Job Match Score")

                    # Get results
                    match_pct = result.get("match_percentage", 0)
                    suitability = result.get("suitability", "Unknown")
                    matched = result.get("matched_skills", [])
                    missing = result.get("missing_skills", [])

                    # Show match percentage and suitability
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Match Percentage", f"{match_pct}%")
                    with col2:
                        # Color based on suitability
                        if suitability == "Excellent":
                            st.success(f"Suitability: {suitability} ✅")
                        elif suitability == "Good":
                            st.info(f"Suitability: {suitability} ✔️")
                        elif suitability == "Moderate":
                            st.warning(f"Suitability: {suitability} ⚠️")
                        else:
                            st.error(f"Suitability: {suitability} ❌")

                    st.divider()

                    # Show matched and missing skills
                    if matched or missing:

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("✅ Matched Skills", len(matched))
                            if matched:
                                st.write("**Your Strengths:**")
                                for skill in matched[:10]:
                                    st.write(f"• {skill}")

                        with col2:
                            st.metric("⚠️ Missing Skills", len(missing))
                            if missing:
                                st.write("**Gaps to Address:**")
                                for skill in missing[:10]:
                                    st.write(f"• {skill}")

                with tab2:
                    st.subheader("Areas to Improve")

                    improvement_areas = result.get("improvement_areas", [])
                    missing_skills = result.get("missing_skills", [])

                    if improvement_areas or missing_skills:
                        st.write("**Key Areas to Develop (by priority):**")
                        for idx, area in enumerate(improvement_areas[:8], 1):
                            st.write(f"{idx}. {area}")

                    st.divider()

                    # Suitability recommendation
                    suitability = result.get("suitability", "Unknown")
                    if suitability == "Excellent":
                        st.success(
                            "✅ You are an excellent fit for this role! Your profile strongly matches the job requirements.")
                    elif suitability == "Good":
                        st.info(
                            "✔️ You have good potential for this role. Develop 1-2 key skills to strengthen your profile.")
                    elif suitability == "Moderate":
                        st.warning(
                            "⚠️ You have some matching skills, but there are notable gaps. Follow the learning plan to prepare.")
                    else:
                        st.error(
                            "❌ This role might be challenging based on current skills. Consider building foundational skills first.")

                with tab3:
                    st.subheader("Personalized Learning Plan")

                    learning_plan = result.get("learning_plan", [])
                    missing_skills = result.get("missing_skills", [])

                    if learning_plan and len(learning_plan) > 0:
                        st.write("**Your Customized Learning Roadmap:**")

                        for idx, phase in enumerate(learning_plan, 1):
                            st.write(f"**{phase}**")

                        st.divider()
                        st.info("""
                        **Suggested Learning Resources:**
                        - **Coursera & Udemy**: Structured courses and certifications
                        - **Official Documentation**: Deep dive into technologies
                        - **GitHub & Open Source**: Hands-on practical experience
                        - **LeetCode/HackerRank**: Coding practice and algorithms
                        - **YouTube**: Tutorials and educational content
                        - **Medium & Blogs**: Articles and best practices
                        - **Contribute to Projects**: Real-world application
                        """)
                    else:
                        st.success(
                            "✅ You already have most skills for this role! Continue to refine and deepen your expertise.")

                with tab4:
                    st.subheader("AI Analysis & Insights")

                    ai_insights = result.get("ai_insights", "")
                    if ai_insights:
                        st.write(ai_insights)
                    else:
                        st.info("Analysis will be displayed here when available")

                    # Match percentage and suitability
                    st.divider()
                    match_pct = result.get("match_percentage", 0)
                    suitability = result.get("suitability", "Unknown")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Match Percentage", f"{match_pct}%")
                    with col2:
                        st.metric("Suitability", suitability)

                    # Action items
                    st.subheader("🎯 Recommended Next Steps")
                    st.write("""
                    1. **Matched Skills** - These are your strengths! Highlight them prominently in your resume and cover letter
                    2. **Missing Skills** - Prioritize learning these based on the phases in the Learning Plan tab
                    3. **Build Portfolio** - Create projects that demonstrate both matched and newly learned skills
                    4. **Gain Experience** - Apply for internships or junior positions to build practical experience
                    5. **Network** - Connect with professionals in this role on LinkedIn and attend relevant meetups
                    6. **Apply Strategically** - Once you've mastered Phase 2 skills, start applying to these roles
                    """)

# ==============================
# Footer
# ==============================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center">
    <p>© 2026 SkillBridge-AI | Built with ❤️ by Vineet Soni</p>
    <p><small>Powered by FastAPI, Streamlit, RAG, and LLM reasoning</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
