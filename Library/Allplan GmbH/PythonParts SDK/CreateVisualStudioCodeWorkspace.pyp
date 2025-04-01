<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>allplan-gmbh\pythonparts-sdk\CreateVisualStudioCodeWorkspace.py</Name>
        <Title>Visual Studio Code workspace</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Visual Studio Code workspace</Text>
        
        <Parameter>
            <Name>Save Location</Name>
            <Text>Save workspace file as</Text>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>FileButton</Name>
                <Text>Save Workspace File</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <ValueDialog>SaveFileDialog</ValueDialog>
                <FileFilter>Workspace files (*.code-workspace)|*.code-workspace|</FileFilter>
            </Parameter>
        </Parameter>
    
        <Parameter>
            <Name>AddNodeVisualScripts</Name>
            <Text>Add VisualScripts</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>UsePylint</Name>
            <Text>Use pylint</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
</Element>