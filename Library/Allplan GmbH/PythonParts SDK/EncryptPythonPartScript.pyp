<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>allplan_gmbh\pythonparts_sdk\EncryptPythonPartScript.py</Name>
        <Title>Encrypt PythonParts script</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Encrypt</Text>

        <Parameter>
            <Name>FileOrDirectory</Name>
            <Text>File or directory</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>RadioButton1</Name>
                <Text>Single file</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>RadioButton2</Name>
                <Text>Directory</Text>
                <Value>2</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RowFile</Name>
            <Text>File</Text>
            <ValueType>Row</ValueType>
            <Visible>FileOrDirectory == 1</Visible>
            <Parameter>
                <Name>FileButton</Name>
                <Text></Text>
                <EventId>1001</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RowDirectory</Name>
            <Text>Directory</Text>
            <ValueType>Row</ValueType>
            <Visible>FileOrDirectory == 2</Visible>
            <Parameter>
                <Name>DirectoryButton</Name>
                <Text></Text>
                <EventId>1002</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RowTargetDirectory</Name>
            <Text>Target directory</Text>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>TargetDirectoryButton</Name>
                <Text></Text>
                <EventId>1003</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RowCreate</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Create</Name>
                <Text>Create</Text>
                <Value></Value>
                <EventId>1010</EventId>
                <ValueType>Button</ValueType>
                <!-- <Enable>(FileOrDirectory == 1 and File or FileOrDirectory == 2 and Directory) and TargetDirectory</Enable> -->
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Parameter>
            <Name>File</Name>
            <Text></Text>
            <Value></Value>>
            <ValueType>String</ValueType>
            <Persistent>MODEL_AND_FAVORITE</Persistent>
        </Parameter>
        <Parameter>
            <Name>Directory</Name>
            <Text></Text>
            <Value></Value>>
            <ValueType>String</ValueType>
            <Persistent>MODEL_AND_FAVORITE</Persistent>
        </Parameter>
        <Parameter>
            <Name>TargetDirectory</Name>
            <Text></Text>
            <Value></Value>>
            <ValueType>String</ValueType>
            <Persistent>MODEL_AND_FAVORITE</Persistent>
        </Parameter>
    </Page>
</Element>