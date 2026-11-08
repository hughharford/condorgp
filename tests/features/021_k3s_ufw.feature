@F_ufw
Feature: Firewall rules only let the cluster's own machines in
  As the owner of a hub-and-spoke k3s cluster whose nodes talk over the internet
  I want every inbound firewall rule limited to my own machines
  So that the Kubernetes ports are never open to the whole internet

  Scenario: No firewall rule in the repo opens a port to everyone
    Given the repository files
    When I read every ufw allow or limit rule
    Then each one is limited to a source address

  Scenario: A hub lets in only the admin, the spokes and the cluster's own networks
    Given the firewall script
    When I generate the rules for a hub with two spokes
    Then SSH is allowed from the admin address only
    And the API port is allowed from the admin and each node only
    And WireGuard and kubelet ports are allowed from each node only
    And nothing else is opened, and in particular not the Flannel VXLAN port

  Scenario: A spoke opens no API port and accepts only its peers and the admin's SSH
    Given the firewall script
    When I generate the rules for a spoke with a hub and one other spoke
    Then SSH is allowed from the admin address only
    And the API port is not opened
    And WireGuard and kubelet ports are allowed from each node only

  Scenario: Everything else is denied, and the SSH rule comes first
    Given the firewall script
    When I generate the rules for a hub with two spokes
    Then incoming traffic is denied by default
    And the SSH rule comes before the default policy and before the firewall is enabled

  Scenario: The script refuses input that would open the cluster to the world
    Given the firewall script
    Then it rejects an admin address of 0.0.0.0/0, an admin address of any, a huge admin range, no admin address, an unknown role, a node address of 0.0.0.0 and an unusable SSH port, and prints no rules for any of them

  Scenario: The script only prints rules unless told to apply them
    Given the firewall script with a recording fake ufw
    When I run it without APPLY
    Then ufw was never called and it says it is a dry run

  Scenario: Applying runs exactly the rules that were printed
    Given the firewall script with a recording fake ufw
    When I run it with APPLY=1
    Then ufw was called with exactly the printed rules, in the same order
