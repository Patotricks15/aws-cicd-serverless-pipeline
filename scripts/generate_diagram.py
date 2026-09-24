"""Generates docs/architecture.drawio for the CI/CD for Serverless Applications project using drawpyo.

Run with: python3 scripts/generate_diagram.py
"""
import os

import drawpyo

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

AWS4_BASE = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;strokeColor=none;"
    "dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
    "fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;"
)

GENERIC_BOX_STYLE = (
    "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;"
    "fontSize=10;fontColor=#7F6000;align=center;"
)

GROUP_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#232F3E;"
    "dashed=1;verticalAlign=top;align=left;spacingLeft=6;spacingTop=6;fontSize=11;fontColor=#232F3E;"
)


def aws_style(icon_name, fill_color):
    return f"{AWS4_BASE}fillColor={fill_color};shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon_name};"


def add_node(page, name, x, y, icon_name, fill_color, width=64, height=64):
    node = drawpyo.diagram.Object(page=page, value=name)
    node.position = (x, y)
    node.geometry.width = width
    node.geometry.height = height
    node.apply_style_string(aws_style(icon_name, fill_color))
    return node


def add_generic_node(page, name, x, y, width=90, height=50):
    node = drawpyo.diagram.Object(page=page, value=name)
    node.position = (x, y)
    node.geometry.width = width
    node.geometry.height = height
    node.apply_style_string(GENERIC_BOX_STYLE)
    return node


def add_group(page, name, x, y, width, height):
    node = drawpyo.diagram.Object(page=page, value=name)
    node.position = (x, y)
    node.geometry.width = width
    node.geometry.height = height
    node.apply_style_string(GROUP_STYLE)
    return node


def add_edge(page, source, target, label=None):
    edge = drawpyo.diagram.Edge(page=page, source=source, target=target, label=label)
    edge.waypoints = "orthogonal"
    edge.endArrow = "block"
    edge.startArrow = "none"
    edge.strokeColor = "#545B64"
    return edge


def build_diagram():
    file = drawpyo.File()
    file.file_name = "architecture.drawio"
    file.file_path = OUTPUT_DIR

    page = drawpyo.Page(file=file)
    page.name = "CI/CD for Serverless Applications"

    # Developer workstation
    developer = add_node(page, "Developer\n(Client)", 40, 40, "client", "#232F3E")
    ide = add_generic_node(page, "IDE", 30, 170, width=80, height=50)
    code_repo = add_node(page, "Code repo\n(CodeCommit)", 190, 160, "codecommit", "#C925D1")

    # CI/CD pipeline
    cicd_service = add_node(page, "CI/CD Service\n(CodePipeline)", 340, 40, "codepipeline", "#C925D1")
    build_stage = add_node(page, "Build\n(CodeBuild)", 340, 170, "codebuild", "#C925D1")
    deploy_stage = add_node(page, "Deploy\n(CloudFormation)", 340, 300, "cloudformation", "#E7157B")

    artifacts_bucket = add_node(page, "Pipeline artifacts\n(S3)", 540, 40, "s3", "#7AA116")

    # CloudFormation stack deployed by the Deploy stage
    stack_group = add_group(page, "CloudFormation stack", 540, 220, 260, 200)

    add_item_fn = add_node(page, "additem\n(Lambda)", 570, 260, "lambda_function", "#ED7100")
    add_item_api = add_node(page, "/additem\n(API Gateway)", 700, 260, "api_gateway", "#E7157B")
    remove_item_fn = add_node(page, "removeitem\n(Lambda)", 570, 350, "lambda_function", "#ED7100")
    remove_item_api = add_node(page, "/removeitem\n(API Gateway)", 700, 350, "api_gateway", "#E7157B")

    add_edge(page, developer, ide)
    add_edge(page, ide, code_repo, "git push")
    add_edge(page, code_repo, cicd_service, "trigger")

    add_edge(page, cicd_service, build_stage)
    add_edge(page, cicd_service, artifacts_bucket, "pipeline artifacts")
    add_edge(page, build_stage, deploy_stage)
    add_edge(page, deploy_stage, add_item_fn, "CloudFormation template")
    add_edge(page, deploy_stage, remove_item_fn)

    add_edge(page, add_item_api, add_item_fn)
    add_edge(page, remove_item_api, remove_item_fn)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file.write()
    print(f"Wrote {os.path.join(OUTPUT_DIR, file.file_name)}")


if __name__ == "__main__":
    build_diagram()
