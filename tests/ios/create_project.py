"""Create an isolated, unsigned Safari UI-test project using only the standard library."""
from pathlib import Path
import plistlib

folder = Path('tests/ios/SafariPreview.xcodeproj')
folder.mkdir(exist_ok=True)
objects = {}

def add(kind, **fields):
    key = f'{len(objects) + 1:024X}'
    objects[key] = dict(isa=kind, **fields)
    return key

source = add('PBXFileReference', lastKnownFileType='sourcecode.swift', path='SafariPreviewTests.swift', sourceTree='<group>')
product = add('PBXFileReference', explicitFileType='wrapper.cfbundle', path='SafariPreviewTests.xctest', sourceTree='BUILT_PRODUCTS_DIR')
products = add('PBXGroup', children=[product], name='Products', sourceTree='<group>')
group = add('PBXGroup', children=[source, products], sourceTree='<group>')
file = add('PBXBuildFile', fileRef=source)
sources = add('PBXSourcesBuildPhase', buildActionMask=2147483647, files=[file], runOnlyForDeploymentPostprocessing=0)
frameworks = add('PBXFrameworksBuildPhase', buildActionMask=2147483647, files=[], runOnlyForDeploymentPostprocessing=0)
settings = {
    'CODE_SIGNING_ALLOWED': 'NO', 'SDKROOT': 'iphoneos',
    'IPHONEOS_DEPLOYMENT_TARGET': '18.0', 'SWIFT_VERSION': '5.0',
    'PRODUCT_BUNDLE_IDENTIFIER': 'net.pdcd.QRPreviewTests',
    'PRODUCT_NAME': '$(TARGET_NAME)', 'GENERATE_INFOPLIST_FILE': 'YES',
    'TARGETED_DEVICE_FAMILY': '1', 'SUPPORTED_PLATFORMS': 'iphoneos iphonesimulator',
    'ENABLE_TESTABILITY': 'YES', 'SWIFT_OPTIMIZATION_LEVEL': '-Onone',
}
target_configs = [add('XCBuildConfiguration', name=name, buildSettings=settings) for name in ('Debug', 'Release')]
config_list = add('XCConfigurationList', buildConfigurations=target_configs, defaultConfigurationName='Debug', defaultConfigurationIsVisible=0)
target = add('PBXNativeTarget', name='SafariPreviewTests', productName='SafariPreviewTests', productType='com.apple.product-type.bundle.ui-testing', productReference=product, buildConfigurationList=config_list, buildPhases=[sources, frameworks], buildRules=[], dependencies=[])
project_configs = [add('XCBuildConfiguration', name=name, buildSettings={}) for name in ('Debug', 'Release')]
project_list = add('XCConfigurationList', buildConfigurations=project_configs, defaultConfigurationName='Debug', defaultConfigurationIsVisible=0)
project = add('PBXProject', attributes={'LastUpgradeCheck': '1640'}, buildConfigurationList=project_list, compatibilityVersion='Xcode 14.0', developmentRegion='en', knownRegions=['en', 'Base'], mainGroup=group, productRefGroup=products, projectDirPath='', projectRoot='', targets=[target])
(folder / 'project.pbxproj').write_bytes(plistlib.dumps({'archiveVersion': '1', 'classes': {}, 'objectVersion': '56', 'objects': objects, 'rootObject': project}))
scheme_dir = folder / 'xcshareddata/xcschemes'
scheme_dir.mkdir(parents=True, exist_ok=True)
reference = f'<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{target}" BuildableName="SafariPreviewTests.xctest" BlueprintName="SafariPreviewTests" ReferencedContainer="container:SafariPreview.xcodeproj"/>'
(scheme_dir / 'SafariPreview.xcscheme').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="1640" version="1.3">
<BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries><BuildActionEntry buildForTesting="YES" buildForRunning="NO" buildForProfiling="NO" buildForArchiving="NO" buildForAnalyzing="YES">{reference}</BuildActionEntry></BuildActionEntries></BuildAction>
<TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv="YES"><Testables><TestableReference skipped="NO">{reference}</TestableReference></Testables></TestAction>
</Scheme>''')
print('Created Safari UI-test project without package dependencies.')
