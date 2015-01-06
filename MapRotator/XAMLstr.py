xaml_str = """<Window 
       xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" 
       xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" 
       Title="Map Rotator 3000" Height="209" Width="640" ResizeMode="NoResize">
    <Grid>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="309*"/>
            <ColumnDefinition Width="57*"/>
            <ColumnDefinition Width="268*"/>
        </Grid.ColumnDefinitions>
        <TextBox x:Name="path" Margin="8,12,119,134" Text="Please Select a File..." VerticalContentAlignment="Center" Grid.ColumnSpan="3"/>
        <Button x:Name="chooseFile" Margin="156,9,7,137" Content="Select a file" Click="openFileDiag" Grid.Column="2"></Button>
        <Label x:Name="Angle" Content="Angle" Margin="13,95,210,49" FontSize="18" RenderTransformOrigin="0.107,0.45"/>
        <ComboBox Margin="10,128,230,32" HorizontalContentAlignment="Center" VerticalContentAlignment="Center">
            <ComboBoxItem x:Name="_90" Content="90" HorizontalAlignment="Center" VerticalAlignment="Center" IsSelected="True"/>
            <ComboBoxItem x:Name="_180" Content="180" HorizontalAlignment="Center" VerticalAlignment="Center"/>
            <ComboBoxItem x:Name="_270" Content="270" HorizontalAlignment="Center" VerticalAlignment="Center"/>
        </ComboBox>
        <Button x:Name="Rotate" Margin="88,104,8,31" Content="ROTATE" FontSize="24" Click="done_message" Grid.ColumnSpan="3"></Button>
        <TextBox x:Name="destinationFolder" Margin="8,58,119,88" Text="Please Select a Folder..." VerticalContentAlignment="Center" Grid.ColumnSpan="3"/>
        <Button x:Name="chooseFolder" Margin="156,58,7,88" Content="Select a folder" Click="openFolderDialog" Grid.Column="2"/>
        <StatusBar x:Name="statusBar" Margin="0,161,0,0" Grid.ColumnSpan="3">
            <StatusBarItem x:Name="results"/>
        </StatusBar>
    </Grid>
</Window>"""
