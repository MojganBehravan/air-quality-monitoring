import subprocess

def run_hdfs_command(cmd):
    full_cmd = ['docker', 'exec', 'namenode'] + cmd
    try:
        subprocess.run(full_cmd, check=True)
        print(f" Command succeeded: {' '.join(cmd)}")
    except subprocess.CalledProcessError:
        print(f" Command failed: {' '.join(cmd)}")

def setup_hdfs_folders():
    # Create raw folder
    run_hdfs_command(['hdfs', 'dfs', '-mkdir', '-p', '/user/hadoop/raw'])
    run_hdfs_command(['hdfs', 'dfs', '-chown', '-R', 'hadoop:hadoop', '/user/hadoop/raw'])

    # Create processed folder
    run_hdfs_command(['hdfs', 'dfs', '-mkdir', '-p', '/user/hadoop/processed'])
    run_hdfs_command(['hdfs', 'dfs', '-chown', 'hadoop:hadoop', '/user/hadoop/processed'])
    run_hdfs_command(['hdfs', 'dfs', '-chown', 'spark', '/user/hadoop/processed'])

if __name__ == '__main__':
    setup_hdfs_folders()
