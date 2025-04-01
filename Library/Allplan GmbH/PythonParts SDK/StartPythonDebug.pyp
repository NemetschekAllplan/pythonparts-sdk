<Element>
    <Script>
        <Name>allplan_gmbh\pythonparts_sdk\StartPythonDebug.py</Name>
        <Title>StartPythonDebug</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
        <Interactor>True</Interactor>
    </Script>
    <Constants>

        <!-- Actions -->
        <Constant>
            <Name>START_LISTEN</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>

        <!-- Current states -->
        <Constant>
            <Name>DOING_NOTHING</Name>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>LISTENING</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>CONNECTED</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>

        <!-- Info texts -->
        <Constant>
            <Name>BEFORE_CONNECTION</Name>
            <Value>To connect your IDE for debugging, follow these steps:\n\n
1.  Click "Start listening".\n\n
    Allplan will start listening for connection from your IDE on port 5678.\n\n
2.  Go to your IDE:\n\n
    Visual Studio Code:\n
    -   Go to tab "Run and Debug" (Ctrl + Shift + D)\n
    -   Select "Attach to Allplan"\n
    -   Start debugging (F5)\n\n
    Visual Studio:\n
    -   Attach to Process\n
    -   Connection type: Python remote\n
    -   Connection target: localhost:5678\n
    -   Enter\n
    -   Select the Python process
            </Value>
            <ValueType>String</ValueType>
        </Constant>
        <Constant>
            <Name>PORT_IN_USE</Name>
            <Value>Allplan is already listening for connection on port 5678.\n
You can close this tool and start debugging in your IDE (e.g. in VS-Code by pressing F5).\n
If that doesn't work, restart Allplan and run this tool again.</Value>
            <ValueType>String</ValueType>
        </Constant>
        <Constant>
            <Name>CLIENT_CONNECTED</Name>
            <Value>Your IDE is attached to Allplan.\nYou can close this tool now.</Value>
            <ValueType>String</ValueType>
        </Constant>

    </Constants>
    <Page>
        <Name>FirstPage</Name>
        <Text>First page</Text>
        <Parameter>
            <Name>DebuggingExpander</Name>
            <Text>Debugging</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ListenButtonRow</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>StartListenButton</Name>
                    <Text>Start listening</Text>
                    <TextDyn>
texts = ['Start listening', 'Listening', 'Connected']
return texts[CurrentState]
                    </TextDyn>
                    <EventId>START_LISTEN</EventId>
                    <ValueType>Button</ValueType>
                    <Enable>CurrentState == 0</Enable>
                </Parameter>
                <Parameter>
                    <Name>OccupiedPortInfo</Name>
                    <TextDyn>
texts = [BEFORE_CONNECTION, PORT_IN_USE, CLIENT_CONNECTED]
return texts[CurrentState]
                    </TextDyn>
                    <TextId>1005</TextId>
                    <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                    <ValueType>Picture</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>InfoExpander</Name>
            <Text>More information</Text>
            <ValueType>Expander</ValueType>
            <Value>True</Value>

            <Parameter>
                <Name>DebugDocRow</Name>
                <Text>How to debug</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>DebugDocButton</Name>
                    <Text>Learn more</Text>
                    <EventId>0</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>GettingStartedDocRow</Name>
                <Text>Getting started with PythonParts</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>GettingStartedDocButton</Name>
                    <Text>Learn more</Text>
                    <EventId>1</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>

        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>CurrentState</Name>
            <Text>CheckBox</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
