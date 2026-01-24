#!/usr/bin/env python3
"""
Vertex AI Agent Engine Deployment Script

Automates deployment, testing, and cleanup of ADK agents to Vertex AI Agent Engine.
Use this script for instructor demonstrations and post-workshop exploration.

Usage:
    # Deploy the travel assistant
    python deploy.py --action deploy

    # Test a deployed agent
    python deploy.py --action test --endpoint "projects/xxx/locations/xxx/reasoningEngines/xxx"

    # Clean up (stop billing!)
    python deploy.py --action cleanup --endpoint "projects/xxx/locations/xxx/reasoningEngines/xxx"

Environment Variables:
    GOOGLE_CLOUD_PROJECT: Your GCP project ID (required)
    GOOGLE_CLOUD_LOCATION: Region for deployment (default: us-central1)
    STAGING_BUCKET: GCS bucket for staging (default: gs://{project}-adk-staging)

See DEPLOYMENT.md for complete documentation.
"""

import os
import sys
import argparse
import asyncio
from typing import Optional


# ============================================================
# CONFIGURATION
# ============================================================

def get_config() -> dict:
    """Get deployment configuration from environment variables."""
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    if not project:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set")
        print("Run: export GOOGLE_CLOUD_PROJECT='your-project-id'")
        sys.exit(1)

    location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')
    staging_bucket = os.environ.get('STAGING_BUCKET', f'gs://{project}-adk-staging')

    return {
        'project': project,
        'location': location,
        'staging_bucket': staging_bucket,
    }


# ============================================================
# DEPLOYMENT
# ============================================================

def deploy_agent() -> str:
    """
    Deploy the travel assistant to Vertex AI Agent Engine.

    Returns:
        str: The resource name (endpoint) of the deployed agent

    Raises:
        Exception: If deployment fails
    """
    import vertexai
    from vertexai import agent_engines
    from vertexai.agent_engines import AdkApp
    from agent import create_agent

    config = get_config()

    print("=" * 60)
    print("Deploying Travel Assistant to Vertex AI Agent Engine")
    print("=" * 60)
    print(f"Project: {config['project']}")
    print(f"Location: {config['location']}")
    print(f"Staging bucket: {config['staging_bucket']}")
    print()

    # Initialize Vertex AI
    print("Initializing Vertex AI...")
    vertexai.init(
        project=config['project'],
        location=config['location'],
        staging_bucket=config['staging_bucket'],
    )

    # Create the agent
    print("Creating agent...")
    agent = create_agent()

    # Wrap in AdkApp for deployment
    print("Creating AdkApp wrapper...")
    adk_app = AdkApp(
        agent=agent,
        enable_tracing=True,
    )

    # Deploy to Agent Engine
    print("Deploying to Agent Engine (this may take 5-10 minutes)...")
    remote_agent = agent_engines.create(
        adk_app=adk_app,
        display_name="travel-assistant-workshop",
        description="ADK Workshop Travel Booking Assistant",
    )

    endpoint = remote_agent.resource_name

    print()
    print("=" * 60)
    print("Deployment Successful!")
    print("=" * 60)
    print(f"Endpoint: {endpoint}")
    print()
    print("To test:")
    print(f"  python deploy.py --action test --endpoint \"{endpoint}\"")
    print()
    print("To cleanup (IMPORTANT - stops billing):")
    print(f"  python deploy.py --action cleanup --endpoint \"{endpoint}\"")

    return endpoint


# ============================================================
# TESTING
# ============================================================

async def test_deployed_agent(endpoint: str) -> None:
    """
    Test a deployed agent with sample queries.

    Args:
        endpoint: The resource name of the deployed agent
    """
    from vertexai import agent_engines

    print("=" * 60)
    print("Testing Deployed Agent")
    print("=" * 60)
    print(f"Endpoint: {endpoint}")
    print()

    # Get the deployed agent
    print("Connecting to agent...")
    remote_agent = agent_engines.get(endpoint)

    # Create a session
    print("Creating session...")
    session = remote_agent.create_session(user_id="test-user")
    print(f"Session ID: {session.id}")
    print()

    # Test queries
    test_queries = [
        "Find flights from San Francisco to Tokyo on March 15",
        "What hotels are available in Tokyo under $200/night?",
        "Remember my budget is $1500",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"--- Test {i} ---")
        print(f"Query: {query}")
        print()

        response_text = ""
        async for event in remote_agent.async_stream_query(
            session_id=session.id,
            message=query
        ):
            # Check for tool calls
            if hasattr(event, 'function_call') and event.function_call:
                print(f"  [Tool: {event.function_call.name}]")

            # Accumulate response
            if event.content:
                response_text += event.content

        print(f"Response: {response_text[:500]}...")
        print()

    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)
    print()
    print("Remember to cleanup when done:")
    print(f"  python deploy.py --action cleanup --endpoint \"{endpoint}\"")


# ============================================================
# CLEANUP
# ============================================================

def cleanup_agent(endpoint: str) -> None:
    """
    Delete a deployed agent to stop billing.

    Args:
        endpoint: The resource name of the deployed agent
    """
    from vertexai import agent_engines

    print("=" * 60)
    print("Cleaning Up Deployed Agent")
    print("=" * 60)
    print(f"Endpoint: {endpoint}")
    print()

    # Confirm deletion
    confirm = input("This will DELETE the agent and stop billing. Continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cleanup cancelled.")
        return

    # Get and delete the agent
    print("Deleting agent...")
    remote_agent = agent_engines.get(endpoint)
    remote_agent.delete()

    print()
    print("=" * 60)
    print("Cleanup Complete!")
    print("=" * 60)
    print("Agent deleted. Billing stopped.")
    print()
    print("Tip: You can also delete the staging bucket if no longer needed:")
    config = get_config()
    print(f"  gsutil rm -r {config['staging_bucket']}")


# ============================================================
# LIST AGENTS
# ============================================================

def list_agents() -> None:
    """List all deployed agents in the project."""
    import vertexai
    from vertexai import agent_engines

    config = get_config()

    # Initialize Vertex AI
    vertexai.init(
        project=config['project'],
        location=config['location'],
    )

    print("=" * 60)
    print("Deployed Agents")
    print("=" * 60)
    print(f"Project: {config['project']}")
    print(f"Location: {config['location']}")
    print()

    agents = list(agent_engines.list())

    if not agents:
        print("No agents deployed.")
        return

    for agent in agents:
        print(f"Name: {agent.display_name}")
        print(f"Resource: {agent.resource_name}")
        print(f"Created: {agent.create_time}")
        print("-" * 40)

    print()
    print(f"Total: {len(agents)} agent(s)")


# ============================================================
# CLI
# ============================================================

def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Deploy, test, and manage ADK agents on Vertex AI Agent Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Deploy:    python deploy.py --action deploy
  Test:      python deploy.py --action test --endpoint "projects/..."
  Cleanup:   python deploy.py --action cleanup --endpoint "projects/..."
  List:      python deploy.py --action list

Environment Variables:
  GOOGLE_CLOUD_PROJECT    Your GCP project ID (required)
  GOOGLE_CLOUD_LOCATION   Region (default: us-central1)
  STAGING_BUCKET          GCS bucket (default: gs://{project}-adk-staging)

For complete documentation, see DEPLOYMENT.md
        """
    )

    parser.add_argument(
        '--action',
        choices=['deploy', 'test', 'cleanup', 'list'],
        required=True,
        help='Action to perform'
    )

    parser.add_argument(
        '--endpoint',
        type=str,
        help='Agent endpoint (required for test/cleanup)'
    )

    args = parser.parse_args()

    # Validate endpoint for actions that require it
    if args.action in ['test', 'cleanup'] and not args.endpoint:
        print(f"Error: --endpoint is required for {args.action} action")
        print("Use --action list to see deployed agents")
        sys.exit(1)

    # Execute action
    if args.action == 'deploy':
        deploy_agent()

    elif args.action == 'test':
        asyncio.run(test_deployed_agent(args.endpoint))

    elif args.action == 'cleanup':
        cleanup_agent(args.endpoint)

    elif args.action == 'list':
        list_agents()


if __name__ == '__main__':
    main()
