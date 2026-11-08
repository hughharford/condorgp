@A_secrets
Feature: Cluster secrets are never committed in readable form
  As the owner of a public repository
  I want every Kubernetes Secret in it to be encrypted
  So that nobody can read my cluster credentials from GitHub

  Scenario: No plaintext Secret manifest is committed
    Given the repository files
    When I list the Kubernetes Secret manifests
    Then every Secret is SOPS-encrypted, an empty shell or a CHANGEME template

  Scenario: The old default credentials are gone from every Secret
    Given the repository files
    When I decode the values of every Secret manifest
    Then none of them is a well-known default password

  Scenario: Encrypted Secret files really are encrypted
    Given the repository files
    When I list the SOPS-encrypted files
    Then each one has SOPS metadata and only ENC tokens as values

  Scenario: Key material and decrypted copies cannot be committed by accident
    Given the repository ignore rules
    Then age keys, decrypted copies and kubeconfigs are ignored
    And the encrypted Secret and the CHANGEME template are not ignored

  Scenario: The repository's own check rejects a plaintext Secret
    Given a scratch git repository using the repo's secrets script
    When I add a plaintext Secret manifest and run the secrets check
    Then the check fails and names the plaintext file
    And the check passes again once the plaintext Secret is removed

  Scenario: Generated secrets are encrypted and only the owner's key opens them
    Given a scratch copy of the secrets tooling and a throwaway age key
    When I generate the encrypted Secret
    Then the file holds none of the generated passwords in readable form
    And the owner's key decrypts it to random 48-character passwords
    And a different age key cannot decrypt it

  Scenario: Applying decrypts in memory straight into kubectl
    Given a scratch copy of the secrets tooling with a generated Secret and a fake kubectl
    When I run the apply command
    Then kubectl receives the decrypted Secret on stdin
    And no decrypted copy is left on disk

  Scenario: The real encrypted cluster Secret is committed for a real recipient
    Given the repository files
    Then the encrypted cluster Secret exists for a real age recipient
